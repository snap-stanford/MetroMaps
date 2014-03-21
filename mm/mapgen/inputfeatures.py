import math

from timeslice import *

## INPUT FEATURES ##
class InputFeature(object):
	def __repr__(self):
		return 'Input Feature'

	def __init__(self, *args):
		pass

	@classmethod
	def analyze_input(cls, all_features, timeslices):
		for feature in cls.__subclasses__():
			feature.report(timeslices)

	def score(self,s):
		return 0
	
	def report(self, timeslices):
		return 'n/a but the score is: %s' % (self.score(timeslices))


class NumberClusters(object):
	def __repr__(self):
		return self.report()

	def __init__(self, timeslices):
		self.timeslices = timeslices

	def score(self):
		timeslices = self.timeslices
		counts = map(lambda x: len(x.clusters), timeslices)
		return sum(counts)

	def report(self):
		return "Total number of clusters: %i" % self.score()


class NumberUniqueWords(object):
	def __repr__(self):
		return self.report()

	def __init__(self, timeslices):
		self.timeslices = timeslices


	def score(self):
		timeslices = self.timeslices
		s = set()
		for timeslice in timeslices:
			for cluster in timeslice.clusters:
				words = cluster.words
				s.update(set(words))
		return len(s)

	def report(self):
		return "Total unique words: %i" % self.score()

class NumberArticles(object):
	def __repr__(self):
		return self.report()

	def __init__(self, num_articles):
		self.number = num_articles

	def score(self):
		return self.number

	def report(self):
		return "Associated articles (num): %i" % self.number

