import sqlite3
import datetime
import time
import os
from decimal import *

class Sqlapi(object):
	
	def __init__(self, name, **kwargs):
		
		self.name = name
		kwargs['name'] = name
		self.timestamp = str(datetime.date.today())
		
		self.datadir = kwargs.get('datadir')
		
		self.ids = []
		self.names = []
		self.symbols = []
		self.price_usd = []
		self.price_btc = []
		self.volume_24h = []
		self.supply = []
		self.perchange_1h = []
		self.perchange_24h = []
		self.perchange_7d = []
		self.updated = []
		
		self.btcdisc = 0
		self.usddisc = 0
		
		self.dpts = ('id', 'name', 'symbol', 'price_usd',
		'price_btc', '24h_volume_usd', 'available_supply',
		'percent_change_1h', 'percent_change_24h', 'percent_change_7d',
		'last_updated')
		
		self.dptsname = ('ids', 'names', 'symbols', 'price_usd',
		'price_btc', 'volume_24h', 'supply',
		'perchange_1h', 'perchange_24h', 'perchange_7d',
		'updated')
		
		self.dbtodate = False
		
		self.getdatals()
		
		self.connectdb()
		initcheck = os.listdir(self.datadir)
		if ".dbinit" not in initcheck:
			print('Database not initialized!')
			self.initnewdb()
			self.dbtodate = True
		
	def connectdb(self):
		self.conn = sqlite3.connect(self.datadir + 'crypcur.db')
		self.c = self.conn.cursor()
		
	def getdatals(self):
		for x in range(0, len(self.dpts)):
			dtype = self.dpts[x]
			dname = self.dptsname[x]
			dfile = dtype + '.data'
			with open(self.datadir + dfile, 'r') as data:
				for line in data:
					line = line.strip()
					com = "self." + dname + ".append('" + line + "')"
					eval(com)
		
	def initnewdb(self):
		print('Creating new SQL database...')
		for x in range(0, len(self.ids)):
			try:
				curc = self.ids[x]
				com = ''' CREATE TABLE ''' + curc + ''' (time real, date text, price_usd real, price_btc float, volume_24h real, supply real, perchange_1h real, perchange_24h real, perchange_7d real, discrepency text)'''
				self.c.execute(com)
				self.conn.commit()
			except sqlite3.OperationalError:
				print('Error reported while creating table for ' + curc + '. Probably a duplicate. (Are you using add.coins?)')
		self.updatedb()
		os.system('echo 1 > ' + self.datadir + '.dbinit')
		
	def addtable(self, curc):
			try:
				com = ''' CREATE TABLE ''' + curc + ''' (time real, date text, price_usd real, price_btc float, volume_24h real, supply real, perchange_1h real, perchange_24h real, perchange_7d real, discrepency text)'''
				self.c.execute(com)
				self.conn.commit()
				print('Table creation successful.')
			except sqlite3.OperationalError:
				print('Error reported while adding a table for ' + curc + '.')
			
	def updatedb(self, updatesql=True):
		if not self.dbtodate:
			print('Updating current database... \n')
			ctime = str(int(time.time()))
			self.ticker()
			for x in range(0, len(self.ids)):
				try:
					curc = self.ids[x]
					
					date = "'" + self.timestamp + "'"
					price_usd = self.price_usd[x]
					price_btc = self.price_btc[x]
					volume_24h = self.volume_24h[x]
					supply = self.supply[x]
					perchange_1h = self.perchange_1h[x]
					perchange_24h = self.perchange_24h[x]
					perchange_7d = self.perchange_7d[x]
					
					discrep = self.costdisc(x, volume_24h)
				except IndexError as e:
					foudcur = False
					info = '\n Error updating index values for ' + curc + '! Message: ' + str(e)
					print(info)
					#with open('add.coins', 'r') as check:
						#line = line.strip()
						#if curc in line:
						#	info = info + '. Currency already detected in add.coins. Probabaly the North Koreans'
						#	foundcur = True
					#if not foundcur:
						#os.system('echo "' + curc + '" >> add.coins
					os.system('echo "' + str(e) + info + '" >> errors.log')
				if updatesql:				
					try:
						com = 'INSERT INTO ' + curc + ' VALUES (' + ctime + ',' + date + ',' + price_usd + ',' + price_btc + ',' + volume_24h + ',' + supply + ',' + perchange_1h + ',' + perchange_24h + ',' + perchange_7d + ',' + discrep + ')'
						self.c.execute(com)
					except:
						print('Error while entering ' + curc + ' data into database. Attempting to create new table.')
						self.addtable(curc)
			self.marketpres()
			print('\nDatabase update complete for ' + str(x + 1) + ' currencies.')
			self.conn.commit()
		else:
			print('Database is up to date.')
		
	def getdat(self, searchterm, currency, datatype):
		sterm = (searchterm,)
		self.c.execute("SELECT * FROM " + currency + " WHERE " + datatype + "=?", sterm)
		result = self.c.fetchone()
		return result
		
	def closedb(self):
		self.conn.close()
		
	def costdisc(self, index, volume):
		getcontext().prec = 8
		discrep = '0'
		btc2usd = Decimal(self.price_usd[0])
		x = index
		realbit = Decimal(self.price_usd[x]) / btc2usd
		realusd = Decimal(self.price_btc[x]) * btc2usd
		difbit = Decimal(self.price_btc[x]) - realbit
		difusd = Decimal(self.price_usd[x]) - realusd
		perusd = int(realusd / Decimal(self.price_usd[x]) * 100 - 100)
		perbit = int(realbit / Decimal(self.price_btc[x]) * 100 - 100)
		
		perusdex = realusd / Decimal(self.price_usd[x]) * 100 - 100
		perbitex = realbit / Decimal(self.price_btc[x]) * 100 - 100
		if perbit != perusd:
			if abs(perbitex) > 0:
				if perbitex > perusdex:
					self.usddisc = self.usddisc + 1
				else:
					self.btcdisc = self.btcdisc + 1
				
			if abs(perbit) > 1:
				if perbit > perusd:
					sug = 'Buy in USD and sell in BTC'
				else:
					sug = 'Buy in BTC and sell in USD'
				data = "\t " + self.symbols[x] + "\t\t\t" + str(perbit) + "/" + str(perusd) + '\t\t' + sug + '\t' + volume
				print(data)
				discrep = str(perbit) + "/" + str(perusd)
		return discrep
		
	def ticker(self):
		getcontext().prec = 8
		tval = 0
		btval = 0
		values = []
		btcvalues = []
		buylist = []
		print('\tBitcoin (BTC) current price: ' + str(self.price_usd[0]) + '\n')
		print('Current portfolio:')
		print('\tCoin:\t\tPrice(USD):\tPrice(BTC):\tBuy Price(BTC):\tHoldings:\tValue(USD):\tValue(BTC):\t%Change:')
		for x in range(0, len(self.symbols)):
			sym = self.symbols[x]
			if sym != 'R':
				with open('watch.coins', 'r') as watch:
					for line in watch:
						line = line.strip()
						if '#' not in line:
							if sym in line:
								#########################
								### Find quanity info ###
								#########################
								start = line.find(',') + 1
								end = line.find('::')
								quan = Decimal(line[start:end])
								val = int(quan * Decimal(self.price_usd[x]))
								btcval = quan * Decimal(self.price_btc[x])
								values.append(str(val))
								btcvalues.append(str(btcval))
								##########################
								if sym != 'BTC':
									###########################
									### Find buy price info ###
									###########################
									start = line.find('::') + 2
									end = line.find(';')
									buyprice = Decimal(line[start:end])
									buylist.append(str(buyprice))
									
									###########################
									
									################################################
									### Calculate % change for buy/current price ###
									################################################
									perform = Decimal(self.price_btc[x]) / Decimal(buyprice) * Decimal(100.0) - Decimal(100.0)
									################################################
									

									buyform = self.formatvalues(str(buyprice))
								else:
									perform = 'N/A'
									buyform = 'N/A\t'
									
								usdform = self.formatvalues(str(self.price_usd[x]))
								btcform = self.formatvalues(str(self.price_btc[x]))
								btcvalform = self.formatvalues(str(btcval))
								quanform = self.formatvalues(str(quan))
								
								name = self.symbols[x]
								
								try:
									if perform > 0:
										perform = '+' + str(perform)
								except TypeError:
									None
								usdval = val	
								if val > 15:
									val = str(val) + ' <--\t\t'
									perform = str(perform) + ' <--'
									name = '\t' + name + ' <--'
									try:
										if perform > 1:
											name = '>!< ' + name
									except TypeError:
										None
								else:
									val = str(val) + '\t\t'
									name = '\t' + name
								if len(name) <= 8:
									name = name + '\t'
								if usdval > 1:
									print(name + '\t' + str(usdform) + '\t' + btcform + '\t' + str(buyform) + '\t' + str(quanform) + '\t ' + str(val) + str(btcvalform) + '\t' + str(perform))
		for x in range(0, len(values)):
			val = Decimal(values[x])
			tval = tval + val
			bval = Decimal(btcvalues[x])
			btval = btval + bval
		print('\n\tTotal value (USD): $' + str(tval) + '\n\tTotal value (BTC): ' +str(btval))
		print('Price discrepencies:')
		print('\tCurrency:\tDiscrepency% BTC/USD\tSuggest:\t\t\t24hr Volume:')
		
	def formatvalues(self, value):
		places = 10
		raw = list(value)
		frmt = []
		length = len(raw)
		if length != places:
			if length > places:
				for x in range(0, places):
					frmt.append(raw[x])
			if length < places:
				for x in range(0, length):
					frmt.append(raw[x])
				addzeros = places - length
				for x in range(0, addzeros):
					frmt.append('0')
			frmt = ''.join(frmt)
			return frmt
		else:
			return str(value)
		
	def marketpres(self):
		print('\nCurrent market pressure:')
		print('\tBuy in BTC: ' + str(self.btcdisc) + '\t Buy in USD: ' + str(self.usddisc) + '\n')
		if self.btcdisc > self.usddisc + 2:
			print('BTC price predicted to drop')
		if self.btcdisc < self.usddisc:
			print('BTC price predicted to rise')
		else:
			print('BTC price predicted to stagnate')
		
