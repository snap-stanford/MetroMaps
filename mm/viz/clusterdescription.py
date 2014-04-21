import logging
import json
from web_generator import WebGeneratorViz

def construct(config):
	return ClusterDescriptionViz(config)

class ClusterDescriptionViz(object):
	# def _get_node(self, cluster_line, nodes):
	# 	if len(cluster_line) == 0:
	# 		print 'done'
	# 		return None

	# 	print "Processing" + cluster_line
	# 	cluster_elements = cluster_line.split()
	# 	print cluster_elements


	# 	cluster_id = cluster_elements[0]



	# 	if cluster_id in nodes:
	# 		return nodes[cluster_id]

	# 	cluster_words = cluster_elements[1:]

	# 	node = {}
	# 	node['id'] = cluster_id
	# 	node['cluster_words'] = cluster_words
	# 	startof_date = len("clusters_")
	# 	year = cluster_id[startof_date:startof_date+4]
	# 	month = cluster_id[startof_date+4:startof_date+6]
	# 	day = cluster_id[startof_date+6:startof_date+8]
	# 	node['time'] = "%s-%s-%s" % (year, month,day)
	# 	node['label'] = " ".join(cluster_words)
	# 	nodes[cluster_id] = node



	# def _read_lines(self):
	# 	nodes = {}
	# 	lines = {}

	# 	with open(self.input_lines_file) as input_f:
	# 		num_total_lines = int(input_f.readline())
	# 		input_f.readline()
	# 		for line_i in range(num_total_lines):
	# 			line = input_f.readline()
	# 			line=line.strip()
	# 			line_description = line
	# 			clusters = []
	# 			line = input_f.readline().strip()
	# 			clusters += [self._get_node(line,nodes)]

	# 			while (len(line) != 0):
	# 				line=input_f.readline().strip()
	# 				clusters += [self._get_node(line,nodes)]
	# 			print '\n\n\nLINE\n--------------'
	# 			print line_description
	# 			print clusters
	# 	# return (nodes, lines)

	def _read_json_input(self):
		with open(self.input_lines_file) as input_f:
			input_json = json.load(input_f)
			nodes = input_json['nodes']
			lines = input_json['lines']
			return (nodes, lines)
		return None


	def __init__(self, config):
		self.input_lines_file = config['input_lines_json']
		self.output = config['final_map_viz_json']
		if config.get('producehtml', False):
			self.producehtml = True
			self.website_output_dir = config['website_output_dir']
			self.webpage_name = config['webpage_name']
		else:
			self.producehtml = False
		# creates .nodes and .lines:
		(self.nodes, self.lines) = self._read_json_input()
		
	def run(self):
		output_viz_json = {"articles": []}
		out_lines = []
		out_nodes = {}
		node_to_lines = {}
		for line in self.lines:
			line_d = {"id": line["id"], "line_label": ", ".join(line['words']), "nodeIDs": line['nodeIDs']}
			out_lines += [line_d]
			for node in line['nodeIDs']:
				current_lines = node_to_lines.get(node, [])
				current_lines += [line["id"]]
				node_to_lines[node] = current_lines

		for nodeid, node in self.nodes.iteritems():
			cluster_words = " ".join(node["words"])
			node_d = {"id": node["id"],
				"articleIDs": {}, "cluster_words": cluster_words,
				"importance": "1", "label": cluster_words,
				"lineIDs": node_to_lines.get(node['id'], []),
				"time": node["time"]}
			out_nodes[node["id"]] = node_d
		output_viz_json["nodes"] = out_nodes
		output_viz_json["lines"] = out_lines

		with open(self.output,'w') as out_f:
			logging.debug('viz.run: starting dump of json file')
			json.dump(output_viz_json, out_f)
			logging.debug('viz dumped to %s' % self.output)

		if self.producehtml:
			wgv = WebGeneratorViz(self.output, self.website_output_dir, self.webpage_name)
			wgv.run()
			final_product = os.path.join(self.website_output_dir, self.webpage_name)
			logging.info('Preview visualization by opening %s' % final_product)




			





