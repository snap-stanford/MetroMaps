# This module is responsible for taking input JSON and outputting clustered data
# The config file is assumed to be on the project path

import subprocess
import logging
import json
import networkx as nx


class ClusterGenerator:
    def __init__(self, config):
        self.input_JSON = config['input_json']
        self.output_JSON = config['output_json']
        with open(self.input_JSON) as f_in:
	        self.timeslices = json.load(f_in)
	        logging.debug('ClusterGenerator loaded %i timeslices' % len(self.timeslices))


	""" This method can be called in parallel 
		timeslice_dict: "doc_data" "
	"""
	def _create_coocurence_graph(self, timeslice_dict):
		g = nx.Graph()
		doc_data = timeslice_dict["doc_data"] # list of documents

		for doc in doc_data:
			token_ids = [t['id'] for t in doc["tokens"]]
			logging.debug('adding path %s to the graph' % str(token_ids))
			g.addPath(token_ids)

		return g
		

    def run(self):
    	logging.debug('Cluster Generator: run begin')
    	g = self._create_coocurence_graph(self.timeslices[0])
    	logging.debug(g.edges())
    	logging.debug(g.nodes())


    	
        





'''





'''
