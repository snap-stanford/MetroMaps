# This module is responsible for taking input JSON and outputting clustered data
# The config file is assumed to be on the project path

import subprocess
import logging
import json
import networkx as nx
import os.path
from itertools import combinations


class ClusterGenerator(object):
    def __init__(self, config):
        self.input_JSON = config['input_json']
        self.output_JSON = config['output_json']
        self.graphing_on = config.get('graphing', False)
        self.graphing_out = config.get('out_graph_dir')
        self.similarity_merge = float(config.get('similarity_merge'))
        self.out_legacy_dir = config.get('out_legacy_dir')
        if not os.path.exists(self.out_legacy_dir):
            logging.info('Created directory %s' % self.out_legacy_dir)
            os.makedirs(self.out_legacy_dir)
        with open(self.input_JSON) as f_in:
            self.timeslices = json.load(f_in)
            logging.debug(str(self))



    def draw_graph(self,graph,file_name):
        #initialze Figure
        if self.graphing_on:
            import matplotlib.pyplot as plt
            import pylab
            plt.figure(num=None, figsize=(20, 20), dpi=80)
            plt.axis('off')
            fig = plt.figure(1)
            pos = nx.spring_layout(graph)
            labels = dict((node_id, node_label) for node_id, node_label in graph.nodes(data=True))
            nx.draw_networkx_nodes(graph,pos)
            nx.draw_networkx_edges(graph,pos)
            nx.draw_networkx_labels(graph,pos,labels=labels)

            cut = 1.0
            xmax = cut * max(xx for xx, yy in pos.values())
            ymax = cut * max(yy for xx, yy in pos.values())
            buf = .15
            xbuf = xmax * buf
            ybuf = ymax * buf
            plt.xlim(0 - xbuf, xmax + xbuf)
            plt.ylim(0 - ybuf, ymax + ybuf)

            plt.savefig(file_name,bbox_inches="tight")
            pylab.close()
            del fig
        else:
            raise Error("Configuration does not allow graphing")

    

    

    def ccg(self, timeslice_dict):
        g = nx.Graph()
        doc_data = timeslice_dict["doc_data"] # list of documents

        for doc in doc_data:

            token_ids = [t['id'] for t in doc["tokens"]]
            g.add_path(token_ids)
            for t in doc["tokens"]:
                g.node[t['id']] = t['plaintext']
        return g

    @property
    def num_timeslices(self):
        return len(self.timeslices)
        
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "ClusterGenerator: %s timeslices" % len(self.timeslices)

    @staticmethod
    def _merge_one_cluster(from_cluster, into_cluster):
        for word in from_cluster:
            into_cluster.append(word)
        return into_cluster

    def _merge_clusters(self, clusters):
        clusters.sort(key=lambda cluster: len(cluster['cluster_tokens']))
        for i in range(len(clusters)):
            current_cluster_item = clusters[i]
            if not current_cluster_item:
                continue
            current_cluster = current_cluster_item.get('cluster_tokens')
            # fix this to be merging dictionaries, not just lists
            for j in range(i+1, len(clusters)):
                potential_parent_item = clusters[j]
                if not potential_parent_item:
                    continue
                potential_parent = potential_parent_item.get('cluster_tokens')
                if ((len(set(current_cluster) & set(potential_parent))/float(len(current_cluster))) > self.similarity_merge):
                    clusters[j]['cluster_tokens'] = ClusterGenerator._merge_one_cluster(current_cluster, potential_parent)
                    clusters[i] = None
        return [cluster for cluster in clusters if cluster]



    def run(self):
        logging.debug('Cluster Generator: run begin')
        self.timeslice_clusters = {}
        for i in range(self.num_timeslices):
            g = self.ccg(self.timeslices[i])
            if self.graphing_on:
                out_file = os.path.join(self.graphing_out, ("graph_timeslice_%s.pdf" % str(i)))
                self.draw_graph(g,out_file)
                logging.debug('Graph written to %s' % out_file)

            clusters = []
            for k in range(max(g.degree_iter(), key=lambda x: x[1])[1]):
                for community in nx.k_clique_communities(g,k+2):
                    cluster_k = []
                    for node in community:
                        #n_dict = {'plain': g.node[node], 'id': node}
                        token = g.node[node]
                        cluster_k += [token]

                    cluster_d = {'cluster_tokens': cluster_k, 'k': k+2}
                    clusters += [cluster_d]

            self.timeslice_clusters[i] = self._merge_clusters(clusters)
        logging.debug('Clusters for all timeslices')


    def write(self):
        if not self.timeslice_clusters:
            logging.error('Run has not been run yet or there are no timeslices available')
        else:
            with open(self.output_JSON, 'w') as outjson:
                json.dump(self.timeslice_clusters, outjson)

            if self.out_legacy_dir: 
                for i in range(len(self.timeslices)):
                    timeslice_start_date = self.timeslices[i]['cluster_start_date']
                    timeslice_end_date = self.timeslices[i]['cluster_end_date']
                    filename = 'clusters_%s_%s' % (timeslice_start_date, timeslice_end_date)
                    with open(os.path.join(self.out_legacy_dir, filename), 'w') as legacy_out_cluster:
                        for cluster in self.timeslice_clusters[i]:
                            tokens = cluster['cluster_tokens']
                            tokens_joined = ', '.join(tokens)
                            num_tokens = len(tokens)
                            text = 'Cluster: %i %s\n' % (num_tokens, tokens_joined)
                            legacy_out_cluster.write(text)




        logging.info('Clusters written to %s' % self.output_JSON)
        logging.info('Legacy clusters written to %s' % self.out_legacy_dir)
