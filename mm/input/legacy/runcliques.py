import os
import sys


infile = sys.argv[1]
outfile = sys.argv[2]
tempfile = sys.argv[3]

os.system("./cliquesmain -i:"+infile+" -o:"+tempfile+" > /dev/null")

os.system("python getchunks.py "+tempfile+" "+outfile)


	
	
