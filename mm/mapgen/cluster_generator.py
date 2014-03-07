# This module is responsible for taking input JSON and outputting clustered data
# The config file is assumed to be on the project path

import subprocess
import logging
import json

class ClusterGenerator:
    def __init__(self, config):
        self.input_JSON = config['input_json']
        self.output_JSON = config['output_json']
        with open(self.input_JSON) as f_in:
	        self.clusters = json.load(f_in)
	        logging.debug('ClusterGenerator loaded %i timeslices' % len(self.clusters))



    def run(self):
    	logging.debug('Cluster Generator: run begin')
    	
        





'''





'''
