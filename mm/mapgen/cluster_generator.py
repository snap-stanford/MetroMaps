# This module is responsible for taking input JSON and outputting clustered data
# The config file is assumed to be on the project path

import subprocess

class ClusterGenerator:
    def __init__(self, config):
        self.input_dir = config['input_dir']
        self.output_dir = config['temporary_dir']




    def run():
        for timeslice_file in os.listdir(self.input_dir):
            timeslice_file_full = os.path.join(self.input_dir, timeslice_file)
            edgelist = os.path.join(self.output_dir, "%s_edgelist" % timeslice_file)
            status = subprocess.call(['./legacy/CreateCoocurrenceGraph', timeslice_file_full, edgelist])
        





'''





'''
