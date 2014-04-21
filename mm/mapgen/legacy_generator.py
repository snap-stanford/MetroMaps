import subprocess
import logging
import generate_all_lines
import get_words_of_line
import candidate_lines_to_map

class LegacyGenerator(object):
	def __init__(self, configs):
		# configs has > cluster_dir (storing clusters in plaintext legacy format) and
		#             > out_dir (directory to which the map will be written)
		self.cluster_dir = configs['cluster_dir']
		self.raw_lines = configs['raw_lines']
		self.line_descriptions = configs['line_descriptions']
		self.chosen_lines = configs['chosen_lines']
		self.chosen_lines_json = configs['chosen_lines_json']


	def run(self):		
		# devnull = open('/dev/null', 'w')
		# process = subprocess.Popen(['python2.7', 'generate_all_lines.py', self.cluster_dir, self.out_dir, 'blank'])
		# retcode = process.wait()
		# logging.info('Generate all lines finished: code %s' % str(retcode))
		generate_all_lines.main(self.cluster_dir, self.raw_lines)
		logging.info('Line generator done. See %s for output' %self.raw_lines)
		get_words_of_line.main(self.raw_lines,self.line_descriptions)
		logging.info('Getting description done. See %s for output' %self.line_descriptions)
		candidate_lines_to_map.main(self.line_descriptions, self.chosen_lines, self.chosen_lines_json)
		logging.info('Getting map done. See %s (and %s) for output' % (self.chosen_lines, self.chosen_lines_json))
