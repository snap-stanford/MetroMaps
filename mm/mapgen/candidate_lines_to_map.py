'''
This file takes all the candidate lines, and chooses
a subset of them to make up the map.

The basic algo:
- sort all lines from longest -> shortest,
ie most desirable->least desirable.
(Generally the longest lines are the best / 
most interesting to look at, so start with them.
An alternative method is to rank by
length*coherence, giving more weight to lines 
that are both long and coherent.)

Then for our algo, we say
for each line in the ranking:
    take that line if there is 'enough incremental coverage'.

'Enough incremental coverage' means that enough clusters in 
the line are unique. This is done by percentage, ie what
percent of a line's clusters are not already covered by lines
that you've chosen?

We make the cutoff percentage higher as you choose more lines,
so that way maps have generally a consistent number of lines
(around 3-5).

That is the core algorithm; everything else is just wrappers
to read in clusters/lines from files.
'''


import logging
import sys
import json

def log(*args):
    result = ""
    for arg in args:
        result+=str(arg)+" "
    sys.stderr.write(result+"\n")
    sys.stderr.flush()

#Store the cluster id and words in the cluster.
class Cluster:
    #informat: clusterid word1 word2 ...
    def __init__(self, line):
        tokens = line.split()
        self.clusterid = tokens[0]
        self.words = set([])
        for word in tokens[1:]:
            self.words.add(word)

    def serialize(self):
        result = self.clusterid+" "
        for word in self.words:
            result+=word[:-1]+" " #remove commas separating the words
        return result

    @property
    def time(self):
        # TODO: change this to extract the year string
        return self.clusterid 

    def toJSON(self):
        cluster_id = self.clusterid
        startof_date = len("clusters_")
        year = cluster_id[startof_date:startof_date+4]
        month = cluster_id[startof_date+4:startof_date+6]
        day = cluster_id[startof_date+6:startof_date+8]
        time = "%s-%s-%s" % (year, month,day)
        json_object = {"id": self.clusterid, "time": time, "words": list(self.words)}
        return json_object


#Store words associated with the line and associated clusters.
class Line:
    '''Format:
    associated line words (ie 'word1 word2 word3 ...')
    clusterAsString
    clusterAsString
    ...

    Ie first associated line words
    then one line per cluster.
    '''
    def __init__(self, inputstring):
        self.clusters = []
        self.words = set([])
        lines = inputstring.split("\n")
        for word in lines[0].split():
            self.words.add(word)

        self.importance = float(lines[1])

        for line in lines[2:]:
            self.clusters.append(Cluster(line))

    def serialize(self):
        result = []
        for word in self.words:
            result.append(word+" ")
        result.append("\n")
        for cluster in self.clusters:
            result.append(cluster.serialize()+"\n")
        return ''.join(result)

    def toJSON(self, existing_nodes={}):
        json_object = {"nodeIDs":[], "words":list(self.words)}
        for cluster in self.clusters:
            clusterJSON = cluster.toJSON()  
            clusterid = clusterJSON["id"]
            if not clusterJSON["id"] in existing_nodes:
                existing_nodes[clusterid] = clusterJSON
            json_object["nodeIDs"] += [clusterid]
        return json_object
        # note: the existing_nodes should be updated
        # by reference
        

'''Store all the candidate lines
and also track the lines you've chosen so far.
Also, for each cluster store all the lines passing
through that cluster.
'''
class AllLines:
    def __init__(self, filelines):
        alllines = filelines.split("\n\n")[1:-1] #skip file header, and one empty section at the end that appears due to an extra newline at the file's end.
        self.lines = []
        for line in alllines:
            self.lines.append(Line(line))
        self.lines.sort(key=lambda line:len(line.clusters), reverse=True) #longest lines first 

        '''Get a map from clusterid to a set of chosen lines that pass through that cluster.
        At first, all clusters are uncovered. Then as we choose lines, we add those lines to the sets/values in our map.'''
        self.clusterid_linescovering = {}
        for line in self.lines:
            for cluster in line.clusters:
                clusterid = cluster.clusterid
                self.clusterid_linescovering[clusterid] = set([])

        self.chosenlines = []

    '''Here we need to note for each cluster in the line
    that the cluster has an additional line passing through it.'''
    def chooseLine(self, line):
        self.chosenlines.append(line)
        for cluster in line.clusters:
            clusterid = cluster.clusterid
            self.clusterid_linescovering[clusterid].add(line)

    def serializeChosenLines(self):
        result = []
        result.append(str(len(self.chosenlines))+"\n") 
        for line in self.chosenlines:
            result.append(line.serialize())
        return "\n".join(result)+"\n"

    def toJSON(self):
        json_object = {'lines': [], 'nodes':{}}
        for i, line in enumerate(self.chosenlines):
            line_json = line.toJSON(json_object["nodes"])
            line_json["id"] = i+1     
            json_object['lines'] += [line_json]     
        return json_object  

    '''Return the number of clusters in the line
    that already have other lines passing through it.'''
    def getNumIntersects(self, line):
        score=0
        for cluster in line.clusters:
            cid = cluster.clusterid
            othersCovering = self.clusterid_linescovering[cid]
            if len(othersCovering)>0: #already hit
                score+=1
        return score
    def getChosenLines(self):
        return self.chosenLines
    '''We should be doing something smart to look at not only
    cluster coverage, but also word coverage. The commented-out
    parts of this function (and some of the functions defined above)
    are made to also look at word coverage.

    We expect to do a very different method of candidateLinesToMap
    selection in production in the near future, in which case this
    file won't be used. If this file is used and you want to look
    at incremental coverage, you should uncomment the code below and make it 
    do something smart.'''
    def enoughCoverage(self, line):
        # chosenlines = self.chosenlines
        # allwords = set([])
        # for cluster in line.clusters:
        #   allwords = allwords.union(cluster.words)

        # wordscores = []
        # for word in allwords:
        #   score = self.marginalWordScore(word, line, chosenlines)
        #   wordscores.append((score,word))

        # wordscores.sort(reverse=True)
        # bestpairs = wordscores[:5]
        # pair = bestpairs[len(bestpairs)/2] #get the 3rd word assuming 5 words
        # score = pair[0]
        return True #in practice return if above cutoff 

    '''Return the lines that should make up the map, using the algorithm described at the 
    top of this file.'''
    def getCrossingLines(self, minlength, startFractionNewNeeded, increment):
        for line in self.lines:
            numlines = len(self.chosenlines)
            fractionNewNeeded = startFractionNewNeeded + increment*numlines
            if len(line.clusters) < minlength:
                break

            numIntersects = self.getNumIntersects(line)
            numClusters = len(line.clusters)
            fractionNew = 1 - (numIntersects/float(numClusters))
            if fractionNew >= fractionNewNeeded and self.enoughCoverage(line):
                self.chooseLine(line)

        if len(self.chosenlines) == 0: #no lines, tiny query
            #Allow 2-node or 1-node lines
            for line in self.lines:
                if len(line.clusters)>=minlength:
                    continue

                numIntersects = self.getNumIntersects(line)
                numClusters = len(line.clusters)
                fractionNew = 1 - (numIntersects/float(numClusters))
                if fractionNew >= fractionNewNeeded and self.enoughCoverage(line):
                    self.chooseLine(line)

def main(infilename, outfile, outfile_json=None):
    logging.debug('Called candidate lines to map with output json %s' %outfile_json)
    
    with open(infilename) as f:
        f = open(infilename)
        candidatelines = AllLines(f.read())

    '''Only consider lines that are >=3 long.
    The cutoff percentage for getting new clusters is
    .3+.15*numberLinesChosen so far.'''
    candidatelines.getCrossingLines(3, .3, .15) 

    # with open(outfile, 'w') as fo:
    #     fo.write(candidatelines.serializeChosenLines())
    if outfile_json:
        with open(outfile_json, 'w') as fo:
            logging.debug('Dumping to JSON file')

            json.dump(candidatelines.toJSON(), fo)


if __name__=='__main__':
    infilename = sys.argv[1]
    outfile = sys.argv[2]

    main(infilename, outfile)
    #if outfile_json: 
    #    with open(outfile_json) as jsonout:
    #        outdict = {}
    #        outdict['lines'] = 
