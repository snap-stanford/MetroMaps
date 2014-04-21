from jinja2 import Template
import os
import shutil
import json

def WebGeneratorViz(object):
	def __init__(self, data, outdir,  webhtml="Metromaps.html"):
		self.data = data
		self.outdir = outdir
		self.webhtml = webhtml
		self.setupok = True
		self.defaultHTML = 'mm/viz/Metromaps.html'
		self.defaultJS_dir = 'mm/viz/Metromaps_Website_files'
		self.defaultJS_datafile = 'final-json.js'
		if (not os.path.exists(self.outdir)):
			logging.error('Out path does not exist: %s' % self.outdir)
			self.setupok = False

	def run(self):
		if not self.setupok:
			logging.error('Aborting web')
			return 
			
		destination_js_dir = s.path.join(self.outdir, self.defaultJS_dir)
		if not os.path.exists(destination_js_dir):
			shutil.copytree(self.defaultJS_dir, self.outdir)
			dhutil.copyfile(self.defaultHTML, os.path.join(self.outdir, self.webhtml))
			logging.debug('Copied js and html files into %s' % self.outdir)
		else:
			logging.warning("%s already exists, so we won't copy the entire js dir" % destination_js_dir)

		with open(self.data) as in_f:
			json_str = in_f.read()
			outfile = os.path.join(self.outdir, self.defaultJS_datafile)
			with open(outfile, 'w') as out_f:
				out_f.write('var finalJSON = %;' % json_str)
				logging.debug('wrote output data file %s' %outfile)


		




	