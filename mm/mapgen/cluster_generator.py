# This module is responsible for taking input JSON and outputting clustered data
# The config file is assumed to be on the project path

import subprocess
import logging
import json
import networkx as nx
import os.path


class ClusterGenerator(object):
    def __init__(self, config):
        self.input_JSON = config['input_json']
        self.output_JSON = config['output_json']
        self.graphing_on = config.get('graphing', False)
        self.graphing_out = config.get('out_graph_dir')
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

    def graph_JSON(self):
        pass

    def ccg(self, timeslice_dict):
        g = nx.Graph()
        doc_data = timeslice_dict["doc_data"] # list of documents

        for doc in doc_data:

            token_ids = [t['id'] for t in doc["tokens"]]
            logging.debug('adding path %s to the graph' % str(token_ids))
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

    def run(self):
        logging.debug('Cluster Generator: run begin')
        for i in range(self.num_timeslices):
            g = self.ccg(self.timeslices[i])
            logging.debug(g.edges())
            logging.debug(g.nodes(data=True))
            if self.graphing_on:
                self.draw_graph(g,os.path.join(self.graphing_out, ("graph_timeslice_%s.pdf" % str(i))))
