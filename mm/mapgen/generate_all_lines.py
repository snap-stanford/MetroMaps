# if low count words appears in several clusters, those clusters should be combined
# sample input line from one time slice:
# Cluster:  44_obama, 23_barack, 4_immigr, 4_mexico, 3_mexican, 2_costa,

# time_slice is an array list of ordered clusters

import sys,os
import os.path
from features import *
from inputfeatures import *
from timeslice import *
# from cluster import *
import timeit
from Queue import PriorityQueue
import logging

FEATURES = [(PersistenceFeature(), .8), (LengthGoodFeature(), .01), (JacardFeature(), .6), (JacardDifferenceFeature(), -.2), (NoOverlapPenalty(), -2)]
INPUT_FEATURES = []
NUM_ROUND_GLOBAL = 400
NUM_ROUND_APART = 400

OUTPUT_LINES = 300

def log(*args):
	logging.debug('')
	result = ""
	for arg in args:
		result+=str(arg)+" "
	sys.stderr.write(result+"\n")
	sys.stderr.flush()

class Timeline():

	features = []
	MAX_LENGTH = 10
	@classmethod
	def set_features(cls, new_feat=[]):
		cls.features = []
		if (len(new_feat)==0):
			global FEATURES 
			cls.features = FEATURES
		else:
			cls.features = new_feat

	def __init__(self,clusters=[]):
		assert(type(clusters)==type([]))
		self.clusters = clusters

	def __len__ (self):

		if len(self.clusters) == 0:
			return 0
		else:
			return (self.clusters[-1].time - self.clusters[0].time)*MAX_LENGTH +\
				   len(self.clusters)

	def __str__(self):
		s = ['\n\nTIMELINE, score %s with %s clusters' % (str(self.evaluate()), str(len(self.clusters)))]
		s += map(lambda cluster : str(cluster), self.clusters)
		return '\n'.join(s)

	def official_str(self):
		s = [str(self.evaluate())] #importance score; can change to be coherence.
		for cluster in self.clusters:
			s += [str(cluster)]
		return "\n".join(s)

	def report_features(self):
		''' return detailed report on how features impact the score '''
		pass

	def add_cluster(self,cluster):
		self.clusters += [cluster]
		return evaluate()


	def generate_successors(self, timeslice):
		
		successors = []
		for cluster in timeslice.clusters:
			successors += [Timeline(self.clusters+[cluster])]

		# successors += [self]
		return successors

	def get_k_best_successors(self, timeslice, k=2):
		successors = []
		for cluster in timeslice.clusters:
			successors += [Timeline(self.clusters+[cluster])]

		return sorted(successors, key=lambda timeline: timeline.evaluate(), reverse=True)[0:k]

	def get_word_count(self, word=None):
		if word:
			count = 0
			for cluster in self.clusters:
				if word in cluster.words:
					count += 1
			return count
		else:
			counts = {}
			for cluster in self.clusters:
				for word in cluster.words:
					counts[word] = counts[word] + 1 if word in counts else 1
			return counts


	def evaluate(self):
		if Timeline.features == []:
			log('ERROR: no features added yet')

		score = 0
		for feature,weight in Timeline.features:
			
			score += weight * feature.score(self)


		return score



def load_data(raw_time_slices):
	time_slices = []
	raw_time_slices.sort(key=lambda x: x[0]) # sort by filename
	for (t, (filename, time_slice_lines)) in enumerate(raw_time_slices):
		time_s = TimeSlice(time_slice_lines, t, filename)
		time_slices += [time_s]
	return time_slices


def choose_lines(lines, max_lines):
	''' 
	chooses lines for next iteration based on breadth and best
	# 1. go through each line and put in priority queue
	# 2. go through each line in priority queue and either accept it based on uniqueuncess or throw back in
	# 3. if length of the current list is below 400, then fill the gap with just the best lines

	# Todo: design a discounting system?
	'''
	s = set()
	taking = []
	remaining = []
	for line in lines:
		clusters = set(line.clusters)
		if len(clusters.difference(s)) > 0:
			# add the set to the 
			taking += [line]
			s.update(clusters)
		else: 
			remaining += [line]

	num_taking = len(taking)
	num_remaining = len(remaining)

	log('in choosing lines, took %s in first round' % str(num_taking))

	max_to_extract = max(max_lines-num_taking, 0)

	taking += remaining[0:min(num_remaining, max_to_extract)]

	return taking

def build_timeline(slices):
	Timeline.set_features()
	timelines_global = []
	#timelines_apart = []	
	
	log('building lines:')
	log('time\tnum_glob\tnum_apart\ttime')
	
	for timeslice in slices: # go through timeslices left to right
		starttime = timeit.timeit()
		timelines_global = sorted(timelines_global, key=lambda timeline: timeline.evaluate(), reverse=True)
		#timelines_apart = sorted(timelines_apart, key=lambda timeline: timeline.evaluate(), reverse=True)
		timelines_global = choose_lines(timelines_global, NUM_ROUND_GLOBAL)
		#timelines_apart = choose_lines(timelines_apart, NUM_ROUND_APART)
		log('starting round wtih %s lines in global' % str(len(timelines_global)))
		#print 'starting round wtih %s lines in apart' % str(len(timelines_apart))
		next_global_timelines = []
		#next_apart_timelines = []
		for timeline in timelines_global:
			# consider the clusters and append to each one 
			successors = timeline.generate_successors(timeslice)
			next_global_timelines += successors

		# now the unsorted lines!
#
		#total_successors = 0
		#for timeline in timelines_apart:

		#	successors = timeline.get_k_best_successors(timeslice,2)
		#	total_successors += len(successors)
			#next_apart_timelines += successors

		for cluster in timeslice.clusters:
				# append good candidates to existing 

			# or start a new one with the current cluster
			#next_apart_timelines += [Timeline([cluster])]
			next_global_timelines += [Timeline([cluster])]

		timelines_global += next_global_timelines
		#timelines_apart += next_apart_timelines

		endtime = timeit.timeit()
		#print '%s\t%s\t%s\t%s' % (str(timeslice.time), str(len(timelines_global)), str(len(timelines_apart)), str(starttime-endtime))
	log('final sort')
	g = sorted(timelines_global, key=(lambda timeline: timeline.evaluate()), reverse=True)
	#a = sorted(timelines_apart, key=(lambda timeline: timeline.evaluate()), reverse=True)
	g = choose_lines(g, OUTPUT_LINES)
	#a = choose_lines(a, OUTPUT_LINES)
	return g

def init_input_features(time_slices, num_articles):
	global INPUT_FEATURES
	INPUT_FEATURES += [(NumberClusters(time_slices), 1)]
	INPUT_FEATURES += [(NumberUniqueWords(time_slices), 1)]
	INPUT_FEATURES += [(NumberArticles(num_articles), 1)]
	
def write_input_stats(file):
	for (feature,weight) in INPUT_FEATURES:
		log(feature)
		file.write(str(feature))
		file.write('\n')


def main(base, outfile):
	''' base should specify the input directory in which clusters are stored '''
	''' outdir should specify the output directory to which the readable line result should be written '''
	''' official_out speicifies the official output directory to which the official output should be written '''
	num_articles = 541	

	indir = os.path.join(base, 'clusters/')

	files = []
	time_slices = []
	for filename in os.listdir(indir):
		files.append(filename)
		f = open(indir + filename)
		lines = f.readlines()
		time_slices.append((filename, lines))
		f.close()
	time_slices = load_data(time_slices)	
	
	init_input_features(time_slices, num_articles)
	instat_filename = outfile+'.in'
	f = open(instat_filename,'w')
	log('In stats at file %s' % instat_filename)
	write_input_stats(f)
	f.close()

	# print 'loaded time_slices, ready to build lines:'
	# for t, time_s in enumerate(time_slices):
	# 	print '\n\n-=-=-=-= TIME %s =-=-=-=-' % str(t)
	# 	print time_s

	#(timelines_global, timelines_apart) = build_timeline(time_slices)
	timelines_global = build_timeline(time_slices)
	log( 'writing...')


	result_global = open(outfile+'.log', 'w')
	#result_apart = open(outdir + 'result_apart', 'w')
	for timeline in timelines_global:
		result_global.write(str(timeline))
	result_global.close()
	# print official output
	result_official = open(outfile,'w')
	# write the header
	result_official.write(str(len(timelines_global)) + '\n\n')
	for timeline in timelines_global:
		result_official.write(timeline.official_str()+'\n\n')
	result_official.close()
	
	#for timeline in timelines_apart:
	#	result_apart.write(str(timeline))

if __name__=='__main__':
	# inputdirectory = CLUSTER_BASE = '../../data/tempfiles/pretty/'
	argv = sys.argv
	if (len(argv) == 4):
		base = sys.argv[1]
		outfile = sys.argv[2]
		query_q = sys.argv[3]
		main(base, outfile)
		sys.exit(0)


	# the below needs to change to have base instead of input dir structure
	inputdirectory = CLUSTER_BASE = 'test_data_in/'
	# append looking at clusters, in addition!! 
	if not os.access(CLUSTER_BASE, os.R_OK):
		log('cannot read cluster_base at %s' %CLUSTER_BASE)



	outputdirectoy = DEFAULT_OUT = 'test_data_out/'
	officialoutput = ''
	# outputdirectoy = DEFAULT_OUT = '../../data/tempfiles/lines/'
	if (len(argv) == 1):
		log(('the following cluster dirs are available:'))

		log(os.listdir(CLUSTER_BASE))
		query = raw_input('Which one?')
		inputdirectory = CLUSTER_BASE + query + '/'
		if not os.access(inputdirectory, os.R_OK):
			log('cannot access input directory %s (for read)' %inputdirectory)

		log('[OK] %s is input directory' % inputdirectory)
		outputdirectory = DEFAULT_OUT + str(query) + '/'

		if not os.access(outputdirectory, os.W_OK):
			log('[WARN] cannot open %s for writing' %outputdirectory)
			raw_input('Press enter to create')
			try:
				os.mkdir(outputdirectory)

			except OSError:
				log( 'ERROR: cannot create directory %s' % outputdirectory)
		raw_input(outputdirectory + ' is output dir. Press Enter to continue.')
	elif(len(argv) == 3):
		inputdirectory = argv[1]
		outputdirectory = argv[2]
	else:
		raise Exception('Wrong argument use')

	main(inputdirectory,outputdirectory)