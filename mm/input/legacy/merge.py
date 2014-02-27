import sys 
filename = sys.argv[1] 
outfile = sys.argv[2]

'''Read file.
Each line of the file is a cluster looking something like this:
Cluster: 7 boston, bomb, finish_line, finished, marathon, line, boston_marathon, 
'''
f = open(filename)
allclusters = []
for line in f.readlines():
	cluster = set([])
	for word in line.split()[2:]: #skip "cluster: 7" and just get the words
		cluster.add(word)
	allclusters.append(cluster)

# lines = f.readlines()
# allclusters = [0]*len(lines)
# for i in range(len(lines)):
# 	line = lines[i]
# 	line = line.split()[2:]
# 	cluster = set([])
# 	for word in line:
# 		cluster.add(word)
# 	allclusters[i] = cluster


allclusters.sort(key=len) #sort low->high so smallest merged with largest first

SUBSET_CUTOFF = .7


def merge(first,second):
	for word in first:
		second.add(word)

#Merge clusters if one is a near-subset of the other, ie
#70% of the words in one cluster are in another cluster
def shouldMerge(first, second):
	smaller = min(len(first), len(second))
	intersect = len(first & second) #first&second  returns intersection
	subset_value = intersect/float(smaller)
	if subset_value > SUBSET_CUTOFF:
		return True
	else:
		return False

for i in range(len(allclusters)): #for each cluster
	for j in range(i+1, len(allclusters)): #for every subsequent cluster
		if shouldMerge(allclusters[i], allclusters[j]):
			merge(allclusters[i], allclusters[j]) #add i words to j
			allclusters[i]=set([]) #delete set
			break

#write clusters to file
f = open(outfile, 'w')
for cluster in allclusters:
	if len(cluster)==0: #don't write out empty/deleted sets
		continue
	f.write("Cluster: ")
	f.write(str(len(cluster))+" ")
	for word in cluster:
		f.write(word+" ")
	f.write("\n")
f.close()


