import os
import datetime
import sqlapi
import subprocess
import time
from subprocess import DEVNULL

class Cryptrack(object):
	'''
	Pull and parse info into SQL db via marketcap.com api
	'''
	
	def __init__ (self, name, **kwargs):
		
		self.name = name
		kwargs['name'] = name
		
		self.adds = False
		self.firstrun = True
		
		self.timestamp = str(datetime.date.today())
		self.cdir = os.getcwd()
		
		self.test = self.initcheck()
		self.datadir = self.cdir + '/data/'
		self.tickdir = self.datadir + 'tick/'
		self.auxdir = self.tickdir + 'aux/'
		
		self.curdata = self.tickdir + self.timestamp + '_tick.data'

		
		self.dpts = ('id', 'name', 'symbol', 'price_usd',
		'price_btc', '24h_volume_usd', 'available_supply',
		'percent_change_1h', 'percent_change_24h', 'percent_change_7d',
		'last_updated')
		
		self.alphnum = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
		
		self.cyclenum = 0
		
		if self.test:
			self.uptodate = self.gettick()
			if self.uptodate:
				self.parsedata()
				###
				self.curmon()
				###
		else:
			input('Fatal Error while creating data directories. Check folder permissions')
	
	def initcheck(self):
		print('Checking data directories...')
		checkdir = os.listdir()
		if "add.coins" in checkdir:
			print('Auxillary coins file found! Enabling auxillary data collection')
			self.adds = True
		if 'data' in checkdir:
			print('Data directory found! Continuing...')
			return True
		else:
			print('Data directories not found. Creating...')
			mkdir = os.system('mkdir -p data/tick/aux')
			if mkdir != 0:
				print('Failure creating directories and data not found! Did you ask nicely for permission?')
				return False
			else:
				print('Data directories created.')
				return True
	
	def gettick(self):

		checktick = os.listdir('data/tick')
		fname = self.timestamp + '_tick.data'
		print('Updating ticker info...')
		cdir = self.tickdir
		check = subprocess.call('wget -O ' + self.curdata + ' https://api.coinmarketcap.com/v1/ticker/', shell=True, stdout=DEVNULL, stderr=DEVNULL)
		
		if check == 0:
			print('Primary Ticker information update successful')
			if self.adds:
				self.getaddticks()
			return True
		else:
			print('Error downloading ticker information')
			return False
			
	def getaddticks(self):
		fail = []
		with open('add.coins', 'r') as adds:
			for line in adds:
				line = line.strip()
				fname = self.auxdir + self.timestamp + '_' + line + '_tick.data'
				check = subprocess.call('wget -O ' + fname + ' https://api.coinmarketcap.com/v1/ticker/' + line, shell=True, stdout=DEVNULL, stderr=DEVNULL)
				if check == 0:
					os.system('cat ' + fname + ' >> ' + self.curdata)
				if check != 0:
					fail.append(line)
			if len(fail) > 0:
				print('Warning: failed to get data for following currencies: ' + str(line))
				
	def fdat(self, string, ststart, stend, startoff=0, endoff=0, sfile=None):
		ilist = []
		if sfile == None:
			sfile = self.curdata
		with open(sfile, 'r') as curdata:
			for line in curdata:
				line = line.strip()
				if string in line:
					start = line.find(ststart) + startoff
					end = line.find(stend) + endoff
					item = line[start:end]
					
					### too specific ###
					if string == '"id": "':
						if '-' in item:
							item = item.replace('-','')
						icheck = list(item)
						try:
							icheck[0] = int(icheck[0])						
							if type(icheck[0]) == int:
								num = icheck[0]
								conv = self.alphnum[num]
								icheck[0] = conv
								item = ''.join(icheck)
						except:
							None
					### end note ###
							
					ilist.append(item)
		return ilist
		
	def getcurrencyls(self):
		print('Detecting currency list...')
		self.currencies = self.fdat('"id":', '"id": "', '",',  startoff=7)
		print('Listing complete. Currencies found:')
		print(self.currencies)
		
	def parsedata(self, updatesql=True):
		self.cyclenum = self.cyclenum + 1
		os.system('clear')
		print('Parsing new data for ' + self.timestamp + ' Cycle: ' + str(self.cyclenum))
		for x in range(0, len(self.dpts)):
			dtype = self.dpts[x]
			dfile = self.datadir + dtype + '.data'
			dstr = '"' + dtype + '": "'
			doffs = len(dstr)
			data = self.fdat(dstr, dstr, '",', startoff=doffs)
			with open(dfile, 'w+') as dfile:
				for i in data:
					dfile.write(i)
					dfile.write('\n')
			#print('Data parsing (' + dtype + ') complete.')
		
		self.updatedb(updatesql)
	
	def updatedb(self, updatesql=True):
		sql = sqlapi.Sqlapi('sql', datadir = self.datadir)
		sql.updatedb(updatesql)
		sql.closedb()
				
	def diff(self):
		sql = sqlapi.Sqlapi('sql', datadir = self.datadir)
		self.discheader()
		info = sql.costdisc()
		sql.closedb()
		
	def curmon(self, freq=.25, dbfreq=8):
		sleepmins = freq * 60
		cycle = 0
		time.sleep(sleepmins)
		while True:
			try:
				cycle = cycle + 1
				self.gettick()
				if cycle != dbfreq:
					self.parsedata(False)
				else:
					self.parsedata()
					cycle = 0
				time.sleep(sleepmins)
			except KeyboardInterrupt:
				input('Ticker process ended by user interrupt. Press enter to continue')
				break
