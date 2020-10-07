import cryptai_v3a

class Finetune(object):
	
	def __init__(self, name, **kwargs):
		
		self.name = name
		kwargs['name'] = name
		
		self.runs = 5

	class results(object):
		totalusd = 0
		totalbtc = 0
		rusd = []
		rbtc = []

	def runsim(self):
		run = cryptai_v3a.Cryptai('a')
		ratiousd, ratiobtc = run.calldata()
		print('USD: \t BTC:')
		print(str(ratiousd) + '\t' + str(ratiobtc))
		self.results.rusd.append(ratiousd)
		self.results.rbtc.append(ratiobtc)

	def start(self):
		for x in range(0, ivar.runs):
			try:
				runsim()
			except:
				None

		for x in range(0, len(results.rusd)):
			self.results.totalusd = self.results.totalusd + self.results.rusd[x]
		avgusd = self.results.totalusd / len(self.results.rusd)

		for y in range(0, len(results.rusd)):
			self.results.totalbtc = self.results.totalbtc + self.results.rbtc[y]
		avgbtc = self.results.totalbtc / len(self.results.rusd)

		with open('avgresults.info', 'w+') as out:
			out.write(str(self.runs) + ' turn average: \n' + str(avgusd) + ' (USD)\n' + str(avgbtc) + ' (BTC)')
