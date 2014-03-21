# from cluster import *

class TimeSlice():
	totals = {}
	non_repeating_totals = {}
	time_to_timeslice = {}
	total_clusters = 0
	
	@classmethod
	def get_wordcount_by_time(cls, time, word=None):
		if word:
			count = 0
			for i in range(time):
				timeslice = TimeSlice.time_to_timeslice[i]
				if word in timeslice.words_in_timeslice:
					count += 1

			return count
		else:
			counts = {}
			for i in range(time):
				timeslice = TimeSlice.time_to_timeslice[i]
				for word in timeslice.words_in_timeslice:
					counts[word] = counts[word] + 1 if word in counts else 1
			return counts

	@classmethod
	def get_total_count(cls, word):
		return TimeSlice.totals[word] if word in TimeSlice.totals else 0

	
	def __init__(self, lines, time, filename):
		self.filename = filename
		self.time = time
		self.words_in_timeslice = set()	

		self.clusters = []
		for i, line in enumerate(lines):
			self.clusters += [Cluster(line, self, i)]

		self.time_counts = {}
		for cluster in self.clusters:
			for word in cluster.words:
				self.words_in_timeslice.add(word)
				TimeSlice.totals[word] = TimeSlice.totals[word]+1 if word in TimeSlice.totals else 1
				self.time_counts[word] = self.time_counts[word]+1 if word in self.time_counts else 1
		TimeSlice.total_clusters += len(self.clusters)
		for word in self.words_in_timeslice:
			TimeSlice.non_repeating_totals[word] = TimeSlice.non_repeating_totals[word]+1 if word in TimeSlice.non_repeating_totals else 1
		
		TimeSlice.time_to_timeslice[time] = self


	def __str__(self):
		clusters_str = [filename]
		for cluster in self.clusters:
			clusters_str += [str(cluster)]
			
		return '\n'.join(clusters_str)

	def isUnique(self,word):
		return (self.time_counts[word] - TimeSlice.totals[word] == 0)

	def prune_clusters(self):
		to_consider = {}

		for cluster in self.clusters:
			for word in cluster.words:
				if TimeSlice.totals[word] == self.time_counts[word] and TimeSlice.totals[word] > 1:
					if word not in to_consider : to_consider[word] = []
					to_consider[word] += cluster.words

		for to_prune in to_consider.values:
			print 'pruning ' + str(to_prune)
			print 'into one: ' + '[not implemented yet, just wanted to see the need]'



class Cluster():
	def __init__(self, line, timeslice, uniqueid):
		if type(line) == type(str()):
			self.words = line.split()[2:]
		else:
			self.words = line
		self.timeslice = timeslice
		self.uniqueid = uniqueid
		
	def __len__(self):
		return len(self.words)

	def __mul__(self, other):
		return [self] * other

	def __rmul__(self, other):
		return self.__mul__(other)

	def __str__(self):
		# with_counts =map(lambda word: ('(%s/%s) =%s' % \
		# 	(str(self.timeslice.time_counts[word]), str(TimeSlice.totals[word]), word)), self.words)

		# return "Time "+ str(self.timeslice.time) + "--   " + " ".join(with_counts)
		return self.timeslice.filename +'_'+ str(self.uniqueid) + " " + (" ".join(self.words))

	def union(self, other):
		return set(self.words).union(set(other.words))

	def intersection(self, other):
		return set(self.words).intersection(set(other.words))

	def get_without_unique(self):
		return Cluster((filter(lambda word: \
			not self.timeslice.isUnique(word), self.words)), self.timeslice, self.uniqueid)
