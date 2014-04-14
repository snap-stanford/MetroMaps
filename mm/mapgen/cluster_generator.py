# This module is responsible for taking input JSON and outputting clustered data
# The config file is assumed to be on the project path

import subprocess
import logging
import json
import sys
import os
import os.path
import snap
from itertools import combinations


class ClusterGenerator(object):
    def __init__(self, config):
        self.input_JSON = config['input_json']
        self.output_JSON = config['output_json']
        self.graphing_on = config.get('graphing', False)
        self.graphing_out = config.get('out_graph_dir')
        self.similarity_merge = float(config.get('similarity_merge'))
        self.dilution_merge = float(config.get('dilution_merge'))
        self.out_legacy_dir = config.get('out_legacy_dir')
        if not os.path.exists(self.out_legacy_dir):
            logging.info('Created directory %s' % self.out_legacy_dir)
            os.makedirs(self.out_legacy_dir)
        with open(self.input_JSON) as f_in:
            self.timeslices = json.load(f_in)
            logging.debug(str(self))



    def draw_graph(self,graph,file_name):
        #initialize Figure
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

    

    

    # def ccg(self, timeslice_dict):
    #     g = nx.Graph()
    #     doc_data = timeslice_dict["doc_data"] # list of documents

    #     for doc in doc_data:

    #         token_ids = [t['id'] for t in doc["tokens"]]
    #         g.add_path(token_ids)
    #         for t in doc["tokens"]:
    #             g.node[t['id']] = t['plaintext']
    #     return g

    def ccg(self, timeslice_dict):
        g = snap.TUNGraph.New()
        doc_data = timeslice_dict["doc_data"]
        node_degrees = {}
        id_to_token = {}
        for doc in doc_data:
            token_ids = [t['id'] for t in doc["tokens"]]
            token_ids = []
            for t in doc["tokens"]:
                tid = t['id']
                token_ids += [tid]
                id_to_token[int(tid)] = t

            for (node_1, node_2) in combinations(token_ids,2):
                if not g.IsNode(int(node_1)):
                    g.AddNode(int(node_1))
                if not g.IsNode(int(node_2)):    
                    g.AddNode(int(node_2))
                g.AddEdge(int(node_1), int(node_2))
                node_degrees[int(node_1)] = node_degrees.get(int(node_1), 0) + 1
                node_degrees[int(node_2)] = node_degrees.get(int(node_2), 0) + 1
        return (g, node_degrees, id_to_token)

    @property
    def num_timeslices(self):
        return len(self.timeslices)
        
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "ClusterGenerator: %s timeslices" % len(self.timeslices)

    @staticmethod
    def _merge_one_cluster(from_cluster, into_cluster):
        into_cluster = from_cluster.union(into_cluster)
        return into_cluster

        ''' Bug #1: not using sets to represents clusters: things get screwed up when using''' 
    def _merge_clusters(self, clusters):
        logging.debug('Starting to merge clusters. At the start they are')

        clusters.sort(key=lambda cluster: len(cluster['cluster_tokens']))
        for cluster in clusters:
            logging.debug(cluster.get('cluster_tokens'))
        for i in range(len(clusters)):
            current_cluster_item = clusters[i]
            if not current_cluster_item:
                continue
            current_cluster = set(current_cluster_item.get('cluster_tokens'))

            # fix this to be merging dictionaries, not just lists
            for j in range(i+1, len(clusters)):
                potential_parent_item = clusters[j]
                if not potential_parent_item:
                    continue
                potential_parent = set(potential_parent_item.get('cluster_tokens'))
                similarity_score = (len(current_cluster & potential_parent)/float(len(current_cluster)))
                potential_merge = ClusterGenerator._merge_one_cluster(current_cluster, potential_parent)
                dilution_score = (len(potential_merge - current_cluster) / float(len(current_cluster)))
                if similarity_score >= self.similarity_merge and dilution_score <= self.dilution_merge:
                    logging.debug('Merging {{{%s}}} into {{{%s}}} (%f similarity) (%f dilution)' \
                            % (str(current_cluster), str(potential_parent), similarity_score, dilution_score) )
                    clusters[j]['cluster_tokens'] = list(ClusterGenerator._merge_one_cluster(current_cluster, potential_parent))
                    clusters[i] = None
                    break
        return [cluster for cluster in clusters if cluster]

    def clique_percolation(self, g, k, id_to_token):
        ''' The following class is for suppressing output '''
        class NullDevice(object):
            def write(self, s):
                pass


        Communities = snap.TIntIntVV()
        # save_sysout = sys.stdout
        # save_syserr = sys.stderr
        # sys.stdout = NullDevice()
        # sys.stderr = NullDevice()
        snap.TCliqueOverlap_GetCPMCommunities(g, k, Communities)
        # sys.stdout = save_sysout
        # sys.stderr = save_syserr
        # devnull.close()
        community_list = []
        for C in Communities:
            cluster_k = []
            for Node in C:
                token = id_to_token[Node]['plaintext']
                cluster_k += [token]
            cluster_d = {'cluster_tokens': cluster_k, 'k': k}
            community_list += [cluster_d]
        return community_list


    def run(self):
        logging.debug('Cluster Generator: run begin')
        self.timeslice_clusters = {}
        for i in range(self.num_timeslices):

            current_timeslice = self.timeslices[i]
            (g, node_degrees, id_to_token) = self.ccg(current_timeslice)
            if self.graphing_on:
                out_file = os.path.join(self.graphing_out, ("graph_timeslice_%s.pdf" % str(i)))
                self.draw_graph(g,out_file)
                logging.debug('Graph written to %s' % out_file)

            clusters = []
            for k in range(2, max(node_degrees.values())-2):
                communities = self.clique_percolation(g, k, id_to_token)
                clusters += communities
                # Communities = snap.TIntIntVV()
                # snap.TCliqueOverlap_GetCPMCommunities(g, k+2, Communities)
                    

                # for C in Communities:
                #     cluster_k = []
                #     for Node in C:
                #         token = id_to_token[Node]['plaintext']
                #         cluster_k += [token]
                #     cluster_d = {'cluster_tokens': cluster_k, 'k': k+2}
                #     clusters += [cluster_d]
            self.timeslice_clusters[i] = self._merge_clusters(clusters)
                # for community in nx.k_clique_communities(g,k+2):
                #     cluster_k = []
                #     for node in community:
                #         #n_dict = {'plain': g.node[node], 'id': node}
                #         token = g.node[node]
                #         cluster_k += [token]

                #     cluster_d = {'cluster_tokens': cluster_k, 'k': k+2}
                #     clusters += [cluster_d]

            #self.timeslice_clusters[i] = self._merge_clusters(clusters)    
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
