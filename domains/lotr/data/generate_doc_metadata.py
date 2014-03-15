#!/usr/local/bin/python2.7


import os
import os.path
import sys
import json

if (len(sys.argv) != 2):
	print "Please enter output json file as second parameter"
	print "./generate_doc_metadata.py doc_meta.json"


BASE_DIR = "rawtext" 
all_files = os.listdir(BASE_DIR)
doc_list = []
all_files.sort(key=lambda x: int(x.split('.')[0]))
for i,f in enumerate(all_files):
    f = {'id': str(i+1), 'name': f, 'timestamp': f.split('.')[0]}
    doc_list.append(f)

json.dump(doc_list, open(sys.argv[1],'w'))

