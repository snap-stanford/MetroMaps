# import abc
import math

from timeslice import *

MU = 0

class GlobalFeature():
	def __repr__(self):
		return 'Global Feature' 

	@classmethod
	def report_all(cls, features, chosen_lines):
		reports = []
		for feature in features:
			reports += [('%s: %s' % (feature[1], feature[0].report(chosen_lines)))]

		return ('--%s--\n' % str(chosen_lines))+'\n'.join(reports)

	def report(self,chosen_lines):
		return '%s: %.3f' % (self.__repr__(), self.score(chosen_lines))

	def score(self,chosen_lines):
		return 0

	def marginal_score(self,chosen_lines, new_line):
		return 0

class CoverageClusterFeature(GlobalFeature):
	def __repr__(self):
		return 'Cluster Coverage'

	def score(self, chosen_lines):
		num_total_clusters = TimeSlice.total_clusters
		sets_covered_clusters = map(lambda line: set(line.clusters), chosen_lines)
		all_chosen_clusters = reduce(lambda x,y: x.union(y), sets_covered_clusters)
		num_chosen_clusters = len(all_chosen_clusters)

		return float(num_chosen_clusters) / float(num_total_clusters) 

	def marginal_score(self, chosen_lines, new_line):
		sets_covered_clusters = map(lambda line: set(line.clusters), chosen_lines)
		all_chosen_clusters = reduce(lambda x,y: x.union(y), sets_covered_clusters)
		set_new_clusters = set(new_line.clusters)
		num_new = len(set_new_clusters.difference(all_chosen_clusters))
		return float(num_new) / 10.0 ## max number of clusters

class NumLinesFeature(GlobalFeature):
	def __repr__(self):
		return 'Number of lines should be normal around %i' % MU

	def __init__(self):
		self.mu = 2.5

	def score_diff(self,diff):
		if diff < 1:
			return 1
		elif diff < 2:
			return .8
		elif diff < 3:
			return .5
		elif diff < 4:
			return .2
		else:
			return 0

	def score(self, chosen_lines):
		num_chosen_lines = len(chosen_lines)
		diff = math.fabs(MU - num_chosen_lines)
		return self.score_diff(diff)

	def marginal_score(self, chosen_lines, new_line):
		current_diff = math.fabs(MU - len(chosen_lines))
		next_diff = math.fabs(MU - (len(chosen_lines) + 1))
		current_score = self.score_diff(current_diff)
		next_score = self.score_diff(next_diff)
		return next_score - current_score

class BlankFeature(GlobalFeature):
	def score(self, chosen_lines):
		return 0

	def marginal_score(self,chosen_lines, new_line):
		return 0

class OverlapPenalty(GlobalFeature):
	def __repr__(self):
		return 'Overlap'

	def __assign_score__(self,num_overlaps,num_clusters):
		proportion = float(num_overlaps) / num_clusters
		if proportion <= .2:
			return 0
		if proportion <= .3:
			return .65
		if proportion <= .4:
			return .95
		else:
			return 1


	def score(self, chosen_lines):
		clusters = set([])
		line_score = 0
		for line in chosen_lines:
			num_overlaps = 0
			
			for cluster in line.clusters:
				if cluster in clusters:
					num_overlaps += 1
				else:
					clusters.add(cluster)
			line_score += self.__assign_score__(num_overlaps, len(line.clusters))
		return 1-(float(line_score) / float(len(chosen_lines)))

	def marginal_score(self, chosen_lines, new_line):
		''' return a penalty for each new cluster that new_line overlaps '''
		clusters = set([])
		for line in chosen_lines:
			for cluster in line.clusters:
				clusters.add(cluster)
		overlaps = 0

		for cluster in new_line.clusters:
			if cluster in clusters:
				overlaps += 1
			
		return 1-(float(overlaps) / float(len(new_line.clusters)))

class HasLengthFeature(GlobalFeature):

	def score(self, chosen_lines):
		good_length = filter(lambda x: len(x.clusters)>1, chosen_lines)
		return float(len(good_length)) / len(chosen_lines)

	def marginal_score(self, chosen_lines, new_line):
		if len(new_line.clusters) > 2:
			return 1
		elif len(new_line.clusters) > 1: 
			return .2
		else:
			return 0


class PenalizeOne(GlobalFeature):
	def score(self, chosen_lines):
		bad_length = filter(lambda x: len(x.clusters)==1, chosen_lines)
		return float(len(bad_length)) / len(chosen_lines)

	def marginal_score(self, chosen_lines, new_line):
		if len(new_line.clusters) == 1:
			return 1
		else:
			return 0

# class Relevancy(GlobalFeature):
# 	def score(self, chosen_lines):
# 		for cluster in chosen_lines.clusters:
# 			for word in cluster:
				

# 	def marginal_score(self, chosen_lines):


class CoverageVarianceFeature(GlobalFeature):

	@classmethod
	def _set_lines(cls, lines):
		s = set([])
		for l in lines:
			for cluster in l.clusters:
				s.update(set(cluster.words))

		return s # set of words in these lines

	def __repr__(self):
		return 'CoverageVarianceFeature'

	def score(self, chosen_lines):
		''' marginal contribution of each line to the corpus '''

		set_of_lines = set(chosen_lines)
		differences = []
		for line in chosen_lines:
			without_line = set_of_lines.difference(set([line]))
			words_without = CoverageVarianceFeature._set_lines(without_line)
			words_of_line = CoverageVarianceFeature._set_lines([line])
			difference = (words_without.union(words_of_line)).difference(words_of_line.intersection(words_without))
			differences.append(len(difference))
		total_differences = reduce (lambda x,y: x+y, differences)
		return float(total_differences) / float(len(differences))

	def marginal_score(self, chosen_lines, new_line):
		words_without = CoverageVarianceFeature._set_lines(chosen_lines)
		words_line = CoverageVarianceFeature._set_lines([new_line])
		words_new = (words_without.union(words_line)).difference(words_line.intersection(words_without)).intersection(words_line)
		
		return float(len(words_new)) / len(words_line)




class UniqueWordsFeature():
	def score(self, chosen_lines):
		''' return prize for each *new* unique sequence that the line covers '''
		''' only returns for the first, not permutation around the same word '''
		return 0

	def marginal_score(self, chosen_lines, new_line):
		''' if there is a new unique word that is covered, then return a prize '''

		return 0


''' Abstract Base Feature class '''
class Feature(object):
	#__metaclass__ = abc.ABCMeta

	def __repr__(self):
		return self.__class__

	def report(self,line):
		return '%s: %.3f' % (self.__repr__(), self.score(line))


	
	#@abc.abstractmethod
	def score(self, line):
		''' return a score on the scale [0, 1] about the current line '''
		return

class PersistenceFeature(Feature):

	def __init__(self):
		Feature.__init__(self)

	def __repr__(self):
		return 'Persistence Feature' 

	def score(self, line):
		if len(line.clusters) > 1:
			score = 0
			num_compared = 0
			line_word_count = line.get_word_count()
			for cluster in line.clusters:
				for word in cluster.words:
					total_times = TimeSlice.non_repeating_totals[word]
					
					score += .8 if total_times in [2,3] and total_times==line_word_count[word] else 0
					score += 1 if total_times in range(4,10) and total_times == line_word_count[word] else 0
					score += .5 if total_times in range(4,10) and (total_times-1)==line_word_count[word] else 0
					score += .65 if total_times in range(7,10) and (total_times-2)==line_word_count[word] else 0
					num_compared += 1

			return float(score) / float(num_compared)
		else:
			return 0


class SingleCluster(Feature):
	def score(self, line):
		if len(line.clusters) == 1:
			return 1
		else: 
			return 0 

class StartedFeature(Feature):
	def score(self, line):
		if len(line.clusters) > 0:
			return 1
		else : 
			return 0

class LengthGoodFeature(Feature):
	def __repr__(self):
		return 'Length is good feature' 

	def score(self, line):
		return .1 * len(line.clusters)


class LengthBadFeature(Feature):
	def score(self, line):
		if len(line.clusters) > 0:
			return 1 - .1 * len(line.clusters)
		else:
			return 0

class JacardSelf(Feature):
	def score(self, line):
		
		all_words_list = map(lambda cluster: cluster.words, line.clusters)
		all_words = [y for x in all_words_list for y in x]

class JacardDifferenceFeature(Feature):
	def __repr__(self):
		return 'Jaccard Difference Feature'

	def __init__(self):
		self.times_called = 0




	def score(self,line):
		if len(line.clusters) == 0:
			return 0
		elif len(line.clusters) == 1:
			return 0


		end = len(line.clusters)
		transitions = zip(line.clusters[0:end-1], line.clusters[1:end])
		score = 0
		rounds = 0
		for a, b in transitions:
			num_different = len(a.union(b).difference(a.intersection(b)))
			num_total = len(a.union(b))
			score += float(num_different) / float(num_total)
			rounds += 1
		return float(score) / float(rounds)

class NoOverlapTwoPenalty(Feature):
	def score(self,line):
		if len(line.clusters) == 0:
			return 0
		elif len(line.clusters) == 1:
			return 0
		elif len(line.clusters) == 2:
			return 0

		end = len(line.clusters)
		transitions = zip(line.clusters[0:end-2], line.clusters[2:end])
		for a, b in transitions:
			num_same = len(a.intersection(b))
			mnum = max(len(a),len(b))
			min_overlap = max(mnum / 4, 2)

			if num_same < min_overlap:
				return 1.0
		return 0


class NoOverlapPenalty(Feature):
	def score(self,line):
		if len(line.clusters) == 0:
			return 0
		elif len(line.clusters) == 1:
			return 0

		end = len(line.clusters)
		transitions = zip(line.clusters[0:end-1], line.clusters[1:end])
		for a, b in transitions:
			num_same = len(a.intersection(b))
			mnum = max(len(a),len(b))
			min_overlap = max(mnum / 4, 2)

			if num_same < min_overlap:
				return 1.0
		return 0

class ConsistencyFeaturePenalty(Feature):
	def __repr__(self):
		return 'Consistency Penalty'

	def score(self,line):
		if len(line.clusters) == 0:
			return 0
		elif len(line.clusters) == 1:
			return 0

			
		end = len(line.clusters)
		num_transitions = len(line.clusters) - 1
		transitions = zip(line.clusters[0] * num_transitions, line.clusters[1:end])

		score = 0
		rounds = 0
		for a, b in transitions:
			num_different = len(a.union(b).difference(a.intersection(b)))
			num_total = len(a.union(b))
			score += float(num_different) / float(num_total)
			rounds += 1

		score_1 = float(score) / float(rounds)	
		if len(line.clusters) > 4:
			transitions = zip(line.clusters[1] * (num_transitions-1), line.clusters[2:end])			
			score = 0
			rounds = 0
			for a, b in transitions:
				num_different = len(a.union(b).difference(a.intersection(b)))
				num_total = len(a.union(b))
				score += float(num_different) / float(num_total)
				rounds += 1
			score_2 = float(score) / float(rounds)
			return (score_1 + score_2) / 2.0
		else:
			return score_1

''' Feature 1: jacardian similarity between each cluster transition'''
class JacardFeature(Feature):
	def __repr__(self):
		return 'Jaccard Transition Feature' 

	def __init__(self, scale_ignore_unique = 0):


		self.times_called = 0
		self._scale_ignore_unique = scale_ignore_unique



	def score(self,line):
		self.times_called += 1

		if len(line.clusters) == 0:
			return 0
		elif len(line.clusters) == 1:
			return 0
		
		end = len(line.clusters)
		transitions = zip(line.clusters[0:end-1], line.clusters[1:end])

		score = 0
		for clustA, clustB in transitions:
			num_union = len(clustA.union(clustB))
			num_inter = len(clustA.intersection(clustB))		
			jaccard_standard = float(num_inter) / float(num_union) if num_union > 0 else 0

			A_without_unique = clustA.get_without_unique()
			B_without_unique = clustB.get_without_unique()


			Awou= A_without_unique.union(B_without_unique)
			Bwou= A_without_unique.intersection(B_without_unique)

			Uwou = A_without_unique.union(B_without_unique)
			Iwou = A_without_unique.intersection(B_without_unique)
			num_union_nonunique = len(Uwou)
			num_inter_nonunique = len(Iwou)

			jaccard_nonunique = float(num_inter_nonunique) / float(num_union_nonunique) \
				if len(Uwou) > 0 else 0

			C_non_unq = self._scale_ignore_unique
			score += C_non_unq * jaccard_nonunique + (1.0 - C_non_unq) * jaccard_standard

		return score / float(len(transitions))
