#!/usr/bin/python2.7
import sys
import os
import os.path
import json

def Main(MapFile, ClusterToDocJson, FlatDir, MapOut):
    cluster_to_doc_dict = None
    with open(ClusterToDocJson) as cl_doc:
        cluster_to_doc_dict = json.load(cl_doc)

    with open(MapFile) as map_in:
        with open(MapOut,'w') as map_out:
            for line in map_in.readlines():
                if 'cluster'==line[:len('cluster')]:
                    cluster_key = line.split()[0]
                    doc_fname = cluster_to_doc_dict[cluster_key]
                    doc_fullfname = os.path.join(FlatDir, doc_fname)
                    with open(doc_fullfname) as doc_json_file:
                        doc_json = json.load(doc_json_file)
                        date = doc_json['date']
                        name = doc_json['name']
                        name_replace = name.replace(' ', '_')
                        name_replace = name_replace.upper()
                        name_replace = name_replace + '_' + date[:4]
                        map_out.write(name_replace)
                        map_out.write(line[len(cluster_key):])
                else:
                    map_out.write(line)
    

    

def usage(fname, args):
    return 'python %s %s' %(fname, " ".join(args))

if __name__=='__main__':
    arg = ['MapFile', 'ClusterToDoc.json', 'FlatDir', 'MapOut']
    if (len(sys.argv) != len(arg)+1):
        print usage(sys.argv[0], arg)
        sys.exit(2)


    
    Main(*sys.argv[1:])
