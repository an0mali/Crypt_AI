
class Symfind(object):

	def __init__ (self, name, **kwargs):
		
		self.name = name
		kwargs['name'] = name
		
		self.fsyms = []
		self.listsyms = []
		self.listnames = []
		
		self.convnames = []
		
		self.run()
		
	def run(self):
		self.loadsims()
		self.loaddatainfo()
		self.compareinfo()
		self.output()
		print('Process complete.')
		
	def loadsims(self):
		print('Loading target symbols.')
		with open('biacur.list', 'r') as findlist:
			for line in findlist:
				line = line.strip()
				start = 0
				end = line.find(',')
				sym = line[start:end]
				self.fsyms.append(sym)
		
	def loaddatainfo(self):
		print('Loading data from ticker info.')
		with open('data/symbol.data', 'r') as symbols:
			for line in symbols:
				line = line.strip()
				self.listsyms.append(line)
				
		with open('data/name.data', 'r') as names:
			for line in names:
				line = line.strip()
				self.listnames.append(line)
	
	def compareinfo(self):
		print('Comparing info...')
		for x in range(0, len(self.fsyms)):
			sym = self.fsyms[x]
			if sym in self.listsyms:
				index = self.listsyms.index(sym)
				name = self.listnames[index]
				self.convnames.append(name)
				
	def output(self):
		print('Creating output file.')
		with open('bianames.list', 'w') as out:
			for x in range(0, len(self.convnames)):
				name = self.convnames[x]
				name = name.replace(' ', '')
				name = name.lower()
				out.write(name)
				out.write('\n')
