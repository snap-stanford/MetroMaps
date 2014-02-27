'''This program returns all clusters associated with a query.

The first argument name is the name of the folder the query results will be in.
We look for the folder
prequery/data/query_results/my_query_name

The ouptut will be in
MapGeneration/data/tempfiles/queryname/clusters; there will be one file for each timeslice.

There will also be tempfolders in
MapGenearation/data/tempfiles/queryname; one folder per timeslice, with tempfiles there.

Each folder will have
 1) edgelist, 2) folder with clusters found at each K-value, 3) chunks from ks, 4) human readable chunks from ks, 
 and 5) merged chunks from ks (this will be a copy of the file in the clusters folder)
'''


import sys
import subprocess
import os
import threading
import shutil
import datetime
import Queue

queryname = sys.argv[1]

config_dir = "../../"
sys.path.append(config_dir)
import config

indir = config.QUERY_RESULTS+queryname 
outdir = config.CLUSTERING_TEMPFILES+queryname 

##################Establish stemid->word map###############################
stemid_word = {}
STEMID_WORD_FILE = config.REPRESENTATIVE_TOKENS 

f = open(STEMID_WORD_FILE)
f = f.readlines()
for line in f:
	line = line.split()
	stemid = line[0]
	word = line[1]
	stemid_word[stemid] = word
###############################

cluster_outdir = outdir+"/clusters" #holds just the final output
meta_file = '%s/%s' % (outdir, 'meta.txt')


def log(*args):
	result = ""
	for arg in args:
		result+=str(arg)+" "
	sys.stderr.write(result+"\n")
	sys.stderr.flush()

if os.path.exists(outdir): #This file shouldn't exist; if it does, we have issues.
	log("ERROR IN CLUSTER_QUERY_CLIQUE, OUTPUT DIRECTORY EXISTS")
	sys.exit(1)

os.mkdir(outdir)

if not os.path.exists(cluster_outdir):
	os.mkdir(cluster_outdir)




def prettify(infile, outfile): #convert to human readable ie stemid->word
	fin = open(infile)
	fout = open(outfile, 'w')
	for line in fin.readlines():
		line = line.split()
		fout.write("Cluster: "+str(len(line))+" ")
		for stemid in line:
			fout.write(stemid_word[stemid]+", ")
		fout.write("\n")
	fin.close()
	fout.close()

def runProcess(argument, procname): #procname is just for printing stuff nicely
	before = datetime.datetime.now()
	status = subprocess.call(argument.split())
	if status!=0: #error
		sys.stderr.write("FAILURE DURING "+ procname.upper()+ ", ABORTING\n")
		os._exit(status)

	after = datetime.datetime.now()
	log(procname+": ", after-before)

def runProcessEdgelist(argument, procname): #procname is just for printing stuff nicely
	before = datetime.datetime.now()
	print 'Calling subprocess with argument %s' % str(argument.split)
	status = subprocess.call(argument.split())
	if status!=0 and status!=1: #error
		sys.stderr.write("FAILURE DURING "+ procname.upper()+ ", ABORTING\n")
		os._exit(status)

	after = datetime.datetime.now()
	log(procname+": ", after-before)

	return status 

def file_stats(filename):
	f = open(filename)
	f.readline()
	numberArticle = int(f.readline())
	return (numberArticle)

def runTimeslice(filename,number_list, lock):
	outfname = filename
	tempdir = outdir+"/"+outfname
	if not os.path.exists(tempdir):
		os.mkdir(tempdir)

	#edgelist
	query_output = indir+"/"+filename
	outfilename = "edgelist" 
	edgelist = tempdir+"/"+outfilename
	procname = "Make edgelist"
	print 'Before calling runProcessEdgeList: calling with %s %s' % (query_output, edgelist)
	status = runProcessEdgelist("./CreateCooccurrenceGraph "+query_output+" "+edgelist, procname)
	if status==1: #not enough articles to cluster
		return

	#cliques
	cliques_allk = tempdir+"/cliques_allk"
	clusters_raw = tempdir+"/clusters_raw" #the clusters from edgelist
	procname = "Clique percolation"
	runProcess("python runcliques.py "+edgelist+" "+clusters_raw+" "+cliques_allk, procname)

	#convert to human-readable
	clusters_pretty = tempdir+"/clusters_pretty"
	prettify(clusters_raw, clusters_pretty)

	#run stats on the query:
	stats = file_stats(indir + '/' + filename)
	lock.acquire()
	number_list[0] = number_list[0] + stats
	log(indir + '/' + filename + ': ' + str(stats))
	lock.release()

	#merge them
	clusters_merged = tempdir+"/clusters_merged"
	procname = "merging"
	runProcess("python merge.py "+clusters_pretty+" "+clusters_merged, procname)
	
	enddest = cluster_outdir+"/clusters_"+filename
	shutil.copy(clusters_merged, enddest)

threads = []
total_list = [0] # to make it mutable by reference
counterLock = threading.Lock()

#We run clustering on each timeslice independently.
for filename in os.listdir(indir):
	mythread = threading.Thread(None, runTimeslice, None, (filename,total_list,counterLock))
	threads.append(mythread)
	mythread.start()

for thread in threads:
	thread.join()

tot_files = total_list[0]
f = open(meta_file,'w')
f.write(str(tot_files) + '\n')
f.close()
