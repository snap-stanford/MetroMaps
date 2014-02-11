#!/usr/local/bin/python2.7


import os
import os.path
import sys
import json

BASE_DIR = "rawtext"
all_files = os.listdir(BASE_DIR)
doc_list = []
all_files.sort(key=lambda x: int(x.split('.')[0]))
for i,f in enumerate(all_files):
    f = {'id': i, 'name': f, 'timestamp': f.split('.')[0]}
    doc_list.append(f)

json.dump(doc_list, open(sys.argv[1],'w'))    
