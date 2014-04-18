import logging


class VizGenerator(object):
	def __init__(self, configs):
		self.input_map = configs.input_map
		self.translator = 