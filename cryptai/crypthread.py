import os
import cryptai_v8
import finetune_v8

class Crypthread(object):

	def __init__(self, name, **kwargs):
		
		self.name = name
		kwargs['name'] = name
		
		
