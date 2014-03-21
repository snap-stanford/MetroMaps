import math
import sys

'''THIS FILE IS NO LONGER IMPORTANT, IE WE HAVE ANOTHER WAY OF CHOOSING
THE  WORDS OF THE LINES THAT COMES LATER. HOWEVER, TO PRESERVE THE
FORMATTING FOR FUTURE PARTS OF THE PIPELINE, WE ARE LEAVING THIS FILE IN.

THIS MEANS YOU MAY DELETE THIS FILE & ELIMINATE THIS STEP OF THE PIPELINE
AS LONG AS YOU ARE SURE TO CHANGE THE FILE FORMAT FOR ALL THE FILES DOWN-
STREAM.'''







# infile = "candidateLines.txt"
# outfile = "candidateLinesWithWords.txt"
if __name__=='__main__':
	infile = sys.argv[1]
	outfile = sys.argv[2]
	main(infile, outfile)

def main(infile, outfile):
	clusterid_cluster = {} #keys: clusterids values: clusters (set of words)
	#allLines = [] #each entry is a line, ie a set of clusterids

	CUTOFF_PERCENTAGE = .3

	def getWords(line):
		linewords = set([]) #this will store all lines that the word contains
		for clusterid in line:
			cluster = clusterid_cluster[clusterid]
			for word in cluster:
				linewords.add(word)
		scores = []
		for word in linewords:
			wordscore = 0
			for clusterid in line:
				cluster = clusterid_cluster[clusterid]
				if word in cluster:
					wordscore+=1
			if wordscore > len(line)*CUTOFF_PERCENTAGE: 
				scores.append((wordscore, word))
		scores.sort()
		scores = scores[::-1] #get high->low scores.
		MAX_ALLOWED_WORDS = 2*int(math.sqrt(len(linewords))) #allow somewhat more words for longer lines
		scores = scores[:MAX_ALLOWED_WORDS]
		return_words = []
		for pair in scores:
			return_words.append(pair[1])
		return return_words

	f = open(infile)
	out = open(outfile, 'w') 
	#out.write(f.readline()) #skip query
	out.write(f.readline()) #skip number of lines
	out.write(f.readline()) # skip newline


	while(True): #for each line
		mapline = set([]) #set of clusterids
		toWrite = []
		toWrite.append(f.readline()) #skip the line importance
		while(True): #for each cluster in the line
			fileline = f.readline()
			toWrite.append(fileline)
			if len(fileline.split()) < 2: #done with a mapline
				break
			fileline = fileline.split()
			clusterid = fileline[0]
			cluster = set([])
			for word in fileline[1:]:
				cluster.add(word) 
			clusterid_cluster[clusterid] = cluster
			mapline.add(clusterid)
		if fileline=="": #eof
			break
		lineWords = getWords(mapline)
		for word in lineWords:
			out.write(word+" ")
		out.write("\n")
		for writeline in toWrite:
			out.write(writeline)
	f.close()
	out.close()



