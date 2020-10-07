

import random
import sqai
import os
from decimal import *


class Cryptai(object):
	
	def __init__(self, **kwargs):
		
		### Note: try adjusting buy function proportionately to USD disburse
		### Note: issue with correlate learning system
		
		#self.name = name
		#kwargs['name'] = name		

		self.debug = False
		self.debugrange = False
		self.masterinfo = False
		self.binancecur = True
		
		self.indecisionpause = True
		
		self.preci = 8
		
		self.feespaid = 0
		self.transactions = 0
		self.primed = False
		
		self.outputcalc = True
		self.dataoutputon = False
		
		########################
		### Learning Control ###
		########################
		self.persistence = kwargs.get('persistence', False)
		self.persistamp = kwargs.get('persistamp', 1)
		self.persistdebug = False
		self.persistnorm = False
		self.learncount = 1
		#self.learningsave = kwargs.get('learningsave', False)
		if self.persistence:
			self.learningsave = True
			
		self.holdingspersist = kwargs.get('holdingspersist', False)
		self.simulate = kwargs.get('simulate', True)
		
		#####################################
		### Finetuning output information ###
		#####################################
		self.finetuning = kwargs.get('finetuning', False)
		
		self.fttrial = kwargs.get('fttrial', None)
		self.ftturn = kwargs.get('ftturn', None)
		self.fttotal = kwargs.get('fttotal', None)
		self.ftavgtime = kwargs.get('ftesttime', None)
		self.ftturntime = kwargs.get('ftturntime', None)
		self.ftattrib = kwargs.get('ftattrib', None)
		self.ftvar = kwargs.get('ftvar', None)
		self.ftallvars = kwargs.get('ftallvars', None)
		self.fttimeremain = kwargs.get('fttimeremain', None)
		self.fttesttime = kwargs.get('fttesttime', None)
		
		self.ftavgusd = kwargs.get('ftavgusd', None)
		self.ftavgbtc = kwargs.get('ftavgbtc', None)
		self.ftmlossbtc = kwargs.get('ftmlossbtc', None)
		self.ftmlossusd = kwargs.get('ftmlossusd', None)
		self.ftmgainusd = kwargs.get('ftmgainusd', None)
		self.ftmgainbtc = kwargs.get('ftmgainbtc', None)
		self.ftrungain = kwargs.get('ftrungain', None)
		self.ftrunloss = kwargs.get('ftrunloss', None)
		self.ftfailrate = kwargs.get('ftfailrate', None)
		self.ftavgfailloss = kwargs.get('ftavgfailloss', None)
		self.ftprevattrib = kwargs.get('ftprevattrib', False)
		
		#######################################
		### Load backed up tuned attributes ###
		#######################################
		
		tuned = []
		print(type('self.ftprevattrib'))
		print(self.ftprevattrib)
		if self.ftprevattrib:
			chk = os.listdir()
			tuned.append(kwargs.get('ftattrib', None))
			if 'tuned.autotune' in chk:
				with open('tuned.autotune', 'r') as atin:
					for line in atin:
						line = line.strip()
						tuned.append(line)
				
			with open('prev.attrib', 'r') as data:
				for line in data:
					line = line.strip()
					
					start = 0
					end = line.find(',')
					var = line[start:end]
					
					if var not in tuned:
					
						start = end + 1
						end = line.find(';')
						val = line[start:end]
						
						kwargs[var] = val
						
					

		'''
		###################################
		###### Independent variables ######
		###################################
		'''
		self.exdatreference = kwargs.get('exdatreference', -791.18079)
		######################################################################
		### Index of independent variables categories for complex learning ###
		######################################################################
		self.indvar = ('startval', 'tweaks', 'thresh')
		
		##########################
		### 0. Starting Variables ###
		##########################
		self.startvar = ('usd_cur', 'usd_val', 'btc_profval', 'basefee', 'disburse', 'minimumcoin')
		
		self.usd_cur = Decimal(kwargs.get('usd_cur', 1000)) #0)
		self.usd_val = self.usd_cur #1
		self.btc_profval = 0 #2
		self.basefee = kwargs.get('basefee', 0.001) #3
		self.initbtcprice = 0
		
		self.btcusdintelstrat = kwargs.get('btcusdintelstrat', True)
		self.btcusdfactor = Decimal(kwargs.get('btcusdfactor', 9.1)) 
		
		#######################
		### 1. Learning tweaks ###
		#######################
		self.tweaks = ('basereward',
		 'basepts',
		 'basepenalty',
		 'gainfactor',
		 'lossfactor',
		 'buyreductionfactor',
		 'baserestore',
		 'exdatbasepts',
		 'exdatgainfactor',
		 'learningthresh',
		 'mindisburse',
		 'disburse',
		 'disbursegain',
		 'preferbuy',
		 'preferbuyset',
		 'usddisburse',
		 'usdminimumdisburse',
		 'minimumcoin',
		 'sellminimum',
		 'usddisbursechangerate',
		 'targetusdfactor',
		 'targetusdbonus',
		 'growthfactor',
		 'correlatebonus',
		 'correlatefactor',
		 'basewait',
		 'waitdisbursethresh',
		 'waitdisbursebonus',
		 'actdisbursethresh',
		 'minimumwait',
		 'sellthresh',
		 'sellfactor',
		 'lowthreshfactor',
		 'sthreshfactor'
		 )
		
		self.sthreshfactor = Decimal(kwargs.get('sthreshfactor', 0.07))
		self.avgvalfactor = Decimal(kwargs.get('avgvalfactor', 0.94672)) ##### FINETUNED
		
		self.basereward = kwargs.get('basereward', 57.2) #0 ##### FINETUNED #####
		self.basepts = int(kwargs.get('basepts', 87.34375)) #1 ##### RETUNED within =/- 4 #####
		self.basepenalty = Decimal(kwargs.get('basepenalty', 1.0121875)) ##### FINETuNED withtin +/- 1 #####

		self.gainfactor = Decimal(kwargs.get('gainfactor', 15)) #2 ##### FINETUNED, maybe re-run
		self.lossfactor = Decimal(kwargs.get('lossfactor', 2.0)) #### FINETUNED
		self.lossadjust = Decimal(kwargs.get('lossadjust', 0))
		self.buyreductionfactor = Decimal(kwargs.get('buyreductionfactor', 1))### NEW, if test good, remove and set reduction to 1
		
		self.baserestore = kwargs.get('baserestore', 0) #3 threshhold at which a choice triggers a restore factor event
		self.restorefactor = kwargs.get('restorefactor', 5) #4 Used to ensure no decision reaches 0 points
		
		self.exdatbasepts = Decimal(kwargs.get('exdatbasepts', 127.0212)) #### FINETUNED within +/- 1 ######
		self.exdatgainfactor = kwargs.get('exdatgainfactor', 0.52) ##### FINETUNED #####
		
		self.learningthresh = Decimal(kwargs.get('learningthresh', 0.003736))##### FINETUNED #####
		
		#########################
		self.disbursestrat = kwargs.get('disbursestrat', False)
		
		self.mindisburse = Decimal(kwargs.get('mindisburse', 0.03)) #Starting disburse amount, raises as learning increases
		self.disburse = self.mindisburse
		self.maxdisburse = Decimal(kwargs.get('disburse', 0.196875)) #4 Maximum investment in a single coin, stopping point of mindisburse
		self.disbursegain = Decimal(kwargs.get('disbursegain', 0.02925)) ##### TUEND ##### #Step of disbursement, occurs when buy fails due to not being able to purchase wanted amount
		self.preferbuy = Decimal(kwargs.get('preferbuy', 0.65)) # Adds points to buy action until disbursement level hits a certain point
		self.preferbuyset = Decimal(kwargs.get('preferbuyset', 48)) # Sets buy to this amount when making action decisions before perferbuy point is reached
		self.prebuyactive = self.disbursestrat
		
		self.usddisburse = Decimal(kwargs.get('usddisburse', 0.35)) ##### TUNED within +/- 1 # Maximum USD holdings at a given time
		self.usdminimumdisburse = Decimal(kwargs.get('usdminimumdisburse', 0.10))
		self.usddisbursestrat = kwargs.get('usddisbursestrat', True)
		
		self.minimumcoin = Decimal(kwargs.get('minimumcoin', 0.0021)) #5 Minimum BTC value of a purchase to be made Note: ran usdfactor with this set at .0022
		self.sellminimum = kwargs.get('sellminimum', 0.002) # Minimum BTC value of coin remaining after a sell if a non 100% sell is to be made
		self.minimumremain = kwargs.get('minimumremain', 0.0032) ##### TUNED, higher values untested #####
		
		self.targetusdstrat = kwargs.get('targetusdstrat', True) # Make buying usd /selling btc more likely if usdval is less than targetusdfactor of usddisburse
		self.usddisbursechangerate = int(kwargs.get('usddisbursechangerate', 110)) ### TUNED within -10/+20 ###
		
		self.targetusdfactor = Decimal(kwargs.get('targetusdfactor', 0.2562))
		self.targetusdbonus = Decimal(kwargs.get('targetusdbonus', 19.864)) ##### TUNED within +/- 3 ##### # Multiplier for decision making if strategy conditions are met
		self.changeduration = kwargs.get('changeduration', 'per7d')
		
		self.checkadjust = kwargs.get('checkadjust', False) # Enables or disables selling currency to free up BTC for USD conversion		
		self.growthfactor = Decimal(kwargs.get('growthfactor', 1.3)) ### If usdtarget not met and not enough btc to purchase usd, sell currencies with this much gain to get btc
		
		self.doubledownstrat = kwargs.get('doubledownstrat', False)
		
		self.correlationstrat = kwargs.get('correlationstrat', True)
		self.correlatebonus = Decimal(kwargs.get('correlatebonus', 2.8)) ##### RETUNED ##### ### Act value increase when correlation is found
		self.correlatefactor = Decimal(kwargs.get('correlatefactor', 1.365)) ##### TUNED ##### ## Adjusts bonus/penality to correlation points
		self.correlatewait = kwargs.get('correlatewait', False)
		
		self.holdingswaitstrat = kwargs.get('holdingswaitstrat', True)
		self.basewait = Decimal(kwargs.get('basewait', 72.1)) ###### RETUNED ######
		self.waitdisbursethresh = Decimal(kwargs.get('waitdisbursethresh', 0.78)) ##### RETUNED #####
		self.waitdisbursebonus = Decimal(kwargs.get('waitdisbursebonus', 1.704))##### RETUNED #####
		self.actdisbursethresh = Decimal(kwargs.get('actdisbursethresh', 0.4781))
		self.minimumwait = Decimal(kwargs.get('minimumwait', 6.64))

		
		###########################
		### 2. Threshhold Strategy ###
		###########################
		self.thresh = ('threshval', 'sellthresh', 'sellfactor')
		
		self.threshval = kwargs.get('threshval', 0) #0
		self.sellthresh = kwargs.get('sellthresh', 1.005) #1 ##### TUNED within +/-0.002 ##### buyprice * sellthresh = price required for basic sell actions
		self.sellfactor = kwargs.get('sellfactor', 1.6048) ##### TUNED within +/- 0.01 ##### #2 buyprice x sellthresh x sellfactor = price required for selloff
		self.lowthreshfactor = kwargs.get('lowthreshfactor', 0.0915) ##### TUNED within +/- 24 ##### # buyprice - sellthresh * lowthreshfactor = if price below this point, basic sell action is enabled.
		
		### Sell learning ###
		self.sellfactorstrat = kwargs.get('sellfactorstrat', False)
		
		### Strategy control ###
		self.predictsell = kwargs.get('predictstrat', True)
		self.selloffstrat = kwargs.get('selloffstrat', True) ##### TUNED #####
		self.selloffcnt = 0
		self.maxusdstrat = kwargs.get('maxusdstrat', True)
		'''
		#####################################
		'''
		
		##############################
		### For end game reference ###
		##############################
		self.starting_btc = 0
		self.starting_usd = self.usd_cur
		
		####################
		### Turn control ###
		####################
		self.turnfreq = kwargs.get('turnfreq', 1)
		self.timeframes = []
		self.totalturns = None
		self.curturn = 1
		self.waitbool = False
		self.turnlimit = 8700
		self.mindata = 8708
		self.turnlength = 0
		self.cooldown = 0
		
		self.cooldownfactor = kwargs.get('cooldownfactor', 0)
		
		### Learning/Decision data structure ###
		self.primedat = ('holdingsinfo', 'exdat', 'holdingsmisc') ### Main Reference list of variable categories for data persistence
		
		self.holdingsinfo = ['holdingsname', 'holdingsamt', 'buyprice', 'buyportion', 'sellportion'] # sub-referece list for persistence
		
		self.holdingsname = []
		self.holdingsamt = []
		
		self.holdingswait = []##
		
		self.buyprice = []
		self.buyportion = []
		self.sellportion = []
		
		self.changeref = ('perchange_1h', 'perchange_24h', 'perchange_7d', 'volume_24h')
		self.exdat = ('per1h', 'per24h', 'per7d', 'vol') # sub-referece list for persistence
		self.per1h = []
		self.per24h = []
		self.per7d = []
		
		self.perchange = []##
		self.vol = []
		
		self.holdingsmisc = ('currency', 'tradecurrency', 'curtuple', 'perchange', 'holdingswait', 'correlate1', 'correlateind') # sub-referece list for persistence
		self.currency = []
		self.tradecurrency = []
		self.curtuple = []
		self.cats = ('currency', 'dpts', 'operand', 'dpts2', 'output', 'action', 'result')
		
		self.dpts = ('price_usd',
		'price_btc', 'volume_24h', 'supply',
		'perchange_1h', 'perchange_24h', 'perchange_7d')
		
		self.action = ('buy', 'sell', 'wait')
		
		self.operand = ('+', '-', '*', '/','>', '<', '==')
		self.opnames = ('add', 'subtract', 'multiply', 'divide','greater than', 'less than', 'equal to')
		
		self.portion = ('0.03', '0.05', '0.10', '0.15', '0.25', '0.33', '0.50', '0.66', '0.75', '1')
		

		self.changeamt = (-15, -10, -8, -5, -3, -2, -1, 1, 2, 3, 5, 8, 10, 15)
		
		self.volumeamt = ('100', '500', '1000', '3000', '5000', '8000')


		self.correlate1 = []
		self.correlateind = []
		
		#########################
		#### Turn-based lists ###
		#########################
		self.turncats = ('curact', 'curattrib', 'curdata', 'curdatatype', 'curdatindex', 'turnlength')
		
		self.curact = []
		
		self.curattrib = []
		
		self.curdata = []
		
		self.curdatatype = []
		
		self.curdatindex = [] ## 0 = raw data, 1 = processed data##
		
		### output current variables, for use in easy adjustment ###
		mde = 'w+'
		variance = '0.25'
		for x in range(0, len(self.tweaks)):
			with open('vars.curattrib', mde) as out:
				var = self.tweaks[x]
				val = eval('str(self.' + var + ')')
				out.write(var + ',' + val + ';' + variance + ';;\n')
				mde = 'a+'

		### initiate system ###
		
		self.db = sqai.Sqai('a')
		
		self.init()
		
	def clearobjs(self):
		for x in range(0, len(self.points.primedat)):
			target = self.points.primedat[x]
			com = "self.points." + target + ' = []'
			exec(com)
		
	class faux(object):
		
		
		'''
		 Faux "wallet" used to calculate actions on all non-purchased currencies. Pretends to buy (self.usd_cur) of each currency,
		 and act on 
		 '''
		primedat = ('holdingsinfo', 'exdat', 'holdingsmisc') ### Main Reference list of variable categories for data persistence
		
		holdingsinfo = ['holdingsname', 'holdingsamt', 'buyprice', 'buyportion', 'sellportion'] # sub-referece list for persistence
		
		holdingsname = []
		holdingsamt = []
		
		holdingswait = []##
		
		buyprice = []
		buyportion = []
		sellportion = []
		
		changeref = ('perchange_1h', 'perchange_24h', 'perchange_7d', 'volume_24h')
		exdat = ('per1h', 'per24h', 'per7d', 'vol') # sub-referece list for persistence
		per1h = []
		per24h = []
		per7d = []
		
		perchange = []##
		vol = []
		
	##################
	## Data Classes ##
	##################
				
	class subaction(object):
		sublist = ('portion', 'analyze')
		
		portion = ('buyportion', 'sellportion')
		analyze = ('linear', 'parallel')
		
	class points(object):
		primedat = ('currency', 'dpts', 'action', 'operand', 'compare', 'correlate1', 'holdingsname', 'buyportion', 'sellportion', 'perchange_1h', 'perchange_24h', 'perchange_7d', 'volume_24h', 'volumeamt')
		
		relist =  ('currency', 'dpts', 'action', 'operand')
		
		currency = []
		dpts = []
		action = []
		operand = []
		compare = []
		
		correlate1 = []
		
		holdingsname = []
		
		buyportion = []
		sellportion = []
		
		linear = []
		parallel = []
		
		perchange_1h = []
		perchange_24h = []
		perchange_7d = []
		volume_24h = []
		
		volumeamt = []
		
	def populatescores(self):
		print('Initializing learning system...')
		
		### Prep action points system ###
		for x in range(0, len(self.points.relist)):
			basepts = self.basepts
			item = self.points.relist[x]
			
			if item != 'correlate':
			
				catlist = 'self.' + item
				append = 'self.points.' + item + '.append(basepts)'
				catls = eval(catlist)
				if item not in self.changeref:
					for x in range(0, len(catls)):
						if catls[x] != 'currency' and catls[x] != 'correlate':
							eval(append)
		
		### Prep portion learning system
		for x in range(0, len(self.portion)):
			self.points.buyportion.append(basepts)
			self.points.sellportion.append(basepts)
		
		### Prep volume, percent change 7d, percent change 1w learning system
		for x in range(0, len(self.changeref) - 1):
			datatarget = self.changeref[x]
			for y in range(0, len(self.changeamt)):
				com = 'self.points.' + datatarget + '.append(' + str(self.exdatbasepts) + ')'
				eval(com)
		for x in range(0, len(self.volumeamt)):
			self.points.volume_24h.append(self.exdatbasepts)
			
		
		### Prep btc holdings ###
		self.points.holdingsname.append(self.basepts)
		
		
	def init(self):
		### Set preferbuy and preferbuyset to proper values based on porfolio, poor coding in original variable- this may be source of bugs in resume function
		#BUG NOTE: These variables are functions of other tuned variables, on multiple resumes these numbers can get tremendously high if this is done in __init__
		self.preferbuy *= self.maxdisburse
		self.preferbuyset *= self.basepts
		
		print('Initializing Crypai...')
		#####################
		### Copy database ###
		#####################
		os.system('cp data/crypcur.db cryptai.db')
		#############################################
		### Check for binance currency names list ###
		#############################################
		test = '1 == 1'
		if self.binancecur:
			test = 'cur in self.tradecurrency'
			check = os.listdir()
			if 'bianames.list' in check:
				found = True
			else:
				found = False
			if not found:
				import symfind
				findnames = symfind.Symfind('a')
			
			with open('bianames.list', 'r') as cnames:
				for line in cnames:
					line = line.strip()
					self.tradecurrency.append(line)	
		
		##########################
		### Pull currency list ###
		##########################

		self.curtuple = self.db.getdat('name', 'sqlite_master', 'type', 'table', 'all')
		for x in range(0, len(self.curtuple)):
			curtup = self.curtuple[x]
			cur = curtup[0]
			check = self.db.getdat('count(*)', cur, None, None, 'count')
			if check[0] > self.mindata:
				if eval(test):
					self.currency.append(cur)
		self.currency.append('usd') #### Add usd

		print('Database copied. Currencies loaded into system: ' + str(len(self.currency)))
		print('Populating base scores...')
		#######################
		### Populate scores ###
		#######################
		self.populatescores()
		####################
		### Purchase BTC ###
		####################
		self.prepgamecur()
		
		if self.persistdebug:
			print(str(self.points.volume_24h))
			input()
			
		if self.persistence:
				check = os.listdir()
				if 'persistent_learning' in check:
					self.loaddata()
				else: ###				Update to catch specific exception
					print('Saved persistent data not located. Starting new.')
					input('Enter to continue')
		os.system ("echo '' > datascores.out")
		
		if self.simulate:
			print('Starting game!')
			while True:
				self.playturn()
				if self.turnlimit < self.curturn:
					break
			self.endgame()
			self.points.correlate1 = []
		else:
			None ##########
	
	def savedata(self):
		if self.persistence:
			print('Saving learned data...')
			sdir = 'persistent_learning/'
			check = os.listdir()
			if 'persistent_learning' not in check:
				os.system('mkdir -p persistent_learning/holdings')
				os.system('mkdir ' + sdir + 'points')
				os.system('echo 1 > .persist')
			else:
				check = os.listdir('persistent_learning')
				if 'learncount' in check:
					with open('persistent_learning/learncount', 'r') as lcount:
						for line in lcount:
							count = int(line.strip())
							self.learncount = count
					com = 'echo ' + str(count + 1) + ' > persistent_learning/learncount'
					os.system(com)
				else:
					os.system('echo 1 > persistent_learning/learncount')
			for x in range(0, len(self.primedat)):
				subcat = eval('self.' + self.primedat[x])
				for y in range(0, len(subcat)):
					if subcat[y] != 'holdingsname':
						targetlist = eval('self.' + subcat[y])
						wmode = 'w+'
						for z in range(0, len(targetlist)):
							with open(sdir + 'holdings/' + subcat[y], wmode) as out:
								out.write(str(targetlist[z]) + '\n')
								wmode = 'a'
			
			for x in range(0, len(self.points.primedat)):
				subcat = eval('self.points.' + self.points.primedat[x])
				wmode = 'w+'
				for y in range(0, len(subcat)):
					with open(sdir + 'points/' + self.points.primedat[x], wmode) as out:
						out.write(str(subcat[y]) + '\n')
						wmode = 'a'
						
			
			print('Save complete')
			
	def loaddata(self):
		check = os.listdir()
		if '.persist' in check:
			
			print('Persistent data found. Loading...')
					
			for x in range(0, len(self.points.primedat)):
				subcat = self.points.primedat[x]
				if subcat != 'correlate1' and subcat != 'holdingsname':
					try:
						with open('persistent_learning/points/' + subcat, 'r') as data:
							#before = eval('self.points.' + subcat)
							ind = 0
							fvals = []
							for line in data:
								line = line.strip()
								fvals.append(float(line))
							
							factor = self.factor(fvals)
							for line in data:
								line = float(line.strip())
								### Normalization ###
								#if int(line) < 0:
								#	line = 0
								#else:
								line *= factor
								#####################
								
								if len(line) > 5:
									op = 'float('
								else:
									op = 'int('

									line, factor = self.normalize(line, factor)
								com = 'self.points.' + subcat + '[' + str(ind) + '] = ' + op + line + ')'
								if self.persistdebug:
									print('Trying: "' + com + '"')
								try:
									exec(com)
								except:
									print('Error loading persistent data')
									input('Press enter to continue')
								ind += 1
						if self.persistdebug:
							ldat = eval('self.points.' + subcat)
							print('Data loaded for: ' + subcat)
							print(ldat)
							input('Press enter to continue')
					except FileNotFoundError:
						print('Data for ' + subcat + ' not found')
			print('Persistence: Points data loaded.')
		
	def factor(self, vals):
		maxval = max(vals)
		rbpts = self.basepts * self.persistamp
		factor = float(self.basepts / maxval)
		return factor
		
		
	def volumecalc(self, currency, price):
		rawvol = self.pulldata('volume_24h', currency, self.curturn, 'one')
		btcvol = Decimal(rawvol) * Decimal(price)
		return btcvol
						
	def pulldata(self, returndata=None, currency=None, turnnum=None, mode='one'):
		if currency == 'usd':
			currency = 'bitcoin'
		if turnnum == None:
			turnnum = self.curturn
		if mode == 'one' or mode == 'count':
			data = self.db.getdat(returndata, currency, 'rowid', turnnum, mode)
			cdat = data[0]
		if mode == 'all':
			dlist = []
			data = self.db.getdat(returndata, currency, 'rowid', turnnum, mode)
			for x in range(0, len(data)):
				rdat = data[x]
				cdat = rdat[0]
				dlist.append(cdat)
				return dlist
		return cdat
		

	def prepgamecur(self):
		prepcur = ('bitcoin', 'usd')
		getcontext().prec = 4
		price = self.pulldata('price_usd', 'bitcoin', self.curturn, 'one')
		self.initbtcprice = price
		amt = Decimal(self.usd_cur) / Decimal(price)
		self.btc_profval = amt
		self.starting_btc = amt
		self.threshval = amt
		usdamt = self.usd_cur - amt * Decimal(price)
		for x in range(0, len(prepcur)):
			buyprice = '1'
			if prepcur[x] == 'usd':
				amt = usdamt
				price = 1 / price
			self.holdingsamt.append(amt)
			self.holdingsname.append(prepcur[x])
			self.buyprice.append(Decimal(price))
			self.points.holdingsname.append(self.basepts)
			self.buyportion.append(1)
			self.holdingswait.append(self.basewait)
			
			for x in range(0, len(self.exdat)):
				target = self.exdat[x]
				com = 'self.' + target + '.append(0)' ########### Update when USD added
				eval(com)

		###############
		### Actions ###
		###############

	def prepbuysell(self, action, mode=None, currency=None):
		getcontext().prec = self.preci
		targetval = 'price_btc'
		if currency == None:
			curpull = self.getrecentcur()
			currency = curpull
		else:
			curpull = currency
		if currency == 'bitcoin' or currency == 'usd':
			targetval = 'price_usd'
			if currency == 'usd':
				curpull = 'bitcoin'
		price = Decimal(self.pulldata(targetval, curpull, self.curturn, 'one'))
		if currency == 'usd':
			price = Decimal(1) / Decimal(price)
		if mode != 'sellthresh' and mode != 'check':
			portionbase, porindex = self.rollportion(action, currency, mode)
		else:
			portionbase = None
			porindex = None
		if mode == 'sellthresh':
			index = self.holdingsname.index(currency)
			self.buyprice[index] = price
		
		return currency, price, portionbase, porindex
		
	def correlateitem(self):
		c1 = self.curattrib[1]
		c2 = self.curattrib[2]
		c3 = self.curattrib[3]
		c4 = self.curdata[4]
		
		coritm = (c1, c2, c3, c4)
		
		return coritm
		
		
	def comparisondat(self, currency):
		getcontext().prec = self.preci
		if self.curattrib[4] != 'Null':
			coritm = self.correlateitem()
			
			ind = self.holdingsname.index(currency)
			self.correlate1.append(coritm)
			self.correlateind.append(ind)
			self.points.correlate1.append(self.basepts)
	
	def correward(self, curindex, buyprice, curprice):
		getcontext().prec = self.preci
		change = Decimal(curprice) - buyprice
		factor = buyprice / Decimal(100.0) * change * self.correlatefactor
		for x in range(0, len(self.correlateind)):
			if self.correlateind[x] == curindex - 2:
				value = Decimal(self.points.correlate1.pop(x))
				modval = float(value * factor)
				self.points.correlate1.insert(x, modval)
				if self.points.correlate1[x] < 1:
					self.points.correlate1[x] == 1
					
	def correlatedecide(self, action, actvalue):
		### If sold at a gain, correlate >
		### If sold at a loss, correlate <
		### If correlate < avg, increase wait
		### if correlate > avg, increase buy
		getcontext().prec = self.preci
		bonus = 0
		coritem = self.correlateitem()
		
		totalpts = Decimal(0)
		corlen = len(self.points.correlate1)
		if corlen > 0:
			for x in range(0, corlen):
				totalpts += Decimal(self.points.correlate1[x])
			

			avgpts = totalpts / Decimal(corlen)

			val = 0
			if coritem in self.correlate1:
				for x in range(0, corlen):
					try:
						if self.correlate1[x] == coritem:
							val += self.points.correlate1[x]
					except IndexError:
						print('self.correlate length: ' + str(len(self.correlate1)) + ' values=' + str(self.correlate1))
						print('self.points.correlate length: ' + str(len(self.points.correlate1)) + ' values=' + str(self.points.correlate1))
						print('self.correlateind length: ' + str(len(self.correlateind)) + ' values=' + str(self.correlateind))
						input()

				if val > avgpts:
					if action == 'buy':
						actvalue *= self.correlatebonus
						#input('Buy')
					
			
				if val < avgpts:
					if action == 'wait':
						actvalue *= self.correlatebonus
						if self.correlatewait:
							self.cooldown += 1
							#input('Wait')
		
		return actvalue
		
						
	def buy(self):
		getcontext().prec = self.preci
		action = 'buyportion'
		found = False
		btcusd = False
		btcoh = Decimal(self.holdingsamt[0])
		
		
		
		currency, price, portionbase, porindex = self.prepbuysell(action, None, None)
		if currency == 'bitcoin' or currency == 'usd':
			btcusd = True
		ohind = 0
		if btcusd:
			if currency == 'bitcoin':
				ohind = 1
			btcoh = Decimal(self.holdingsamt[ohind])
		puramount = Decimal(btcoh) / Decimal(price) * Decimal(portionbase)
		purcost = Decimal(puramount) * Decimal(price)
		
		btcmin = self.minimumcoin
		
		#####################################################
		### Buy at least minimum amount, if not then stop ###
		#####################################################
		if purcost < btcmin:
			while True:
				try:
					porindex = porindex + 1
					portionbase = self.portion[porindex]
					puramount = Decimal(btcoh) / Decimal(price) * Decimal(portionbase)
					purcost = Decimal(puramount) * Decimal(price)
					if purcost >= (self.minimumcoin):
						break
				except IndexError:
					print("Tried to buy, but couldn't afford the minimum!")
					self.curdata.append('None')
					return None
		######################################################
		
		##################################################
		### Ensure not all $$$ is invested in one coin ###
		### and try to adjust if so					   ###
		##################################################
		disfactor = self.btc_profval * Decimal(self.disburse)
		if purcost > disfactor:
			while True:
				try:
					porindex = porindex - 1
					portionbase = self.portion[porindex]
					puramount = Decimal(btcoh) / Decimal(price) * Decimal(portionbase)
					purcost = Decimal(puramount) * Decimal(price)
					if purcost <= disfactor and purcost >= btcmin:
						break
				except IndexError:
					print("I wanted to buy, had enough to buy, but don't want all my eggs in one basket!")
					if self.disburse < self.maxdisburse:
						self.disburse = self.disburse + self.disbursegain
					self.curdata.append('None')
					return None
		
		if Decimal(btcoh) - Decimal(purcost) > Decimal(0.0):
			self.holdingsamt[ohind] = self.holdingsamt[ohind] - purcost
			############################
			### Grab addiitonal data ###
			############################
			if btcusd:
				orig = currency
				currency = 'bitcoin'
			per1h, per24h, per7d, vol = self.pullexdat(currency)
			if btcusd:
				currency = orig
			
			#############################
			
			####################
			### include fees ###
			####################
			self.calcfees(puramount, price, currency)#Keep track of fees paid
			fee = Decimal(puramount) * Decimal(self.basefee)
			puramount = Decimal(puramount) - Decimal(fee)
			####################
			
			try:
				index = self.holdingsname.index(currency)
				found = True
			except ValueError:
				found = False
			if not found:
				index = None

			self.updatedata(currency, puramount, price, per1h, per24h, per7d, vol, found, porindex, index, 'buy')
			self.comparisondat(currency)
			if self.disburse < self.maxdisburse:
				self.disburse = self.disburse + self.disbursegain
		else:
			print("Tried to buy, but couldn't afford it!")
			self.curdata.append('None')
			
	def calcfees(self, puramount, price, currency):
		if currency != 'bitcoin':
			btcequivfee = Decimal(puramount) * Decimal(price) * Decimal(self.basefee)
		else:
			btcequivfee = Decimal(puramount) * Decimal(self.basefee)
		self.feespaid += Decimal(btcequivfee)
		self.transactions += 1
			
	def pullexdat(self, currency):
		price = self.pulldata('price_btc', currency, self.curturn, 'one')
		per1h = self.pulldata('perchange_1h', currency, self.curturn, 'one')
		per24h = self.pulldata('perchange_24h', currency, self.curturn, 'one')
		per7d = self.pulldata('perchange_7d', currency, self.curturn, 'one')
		vol = self.volumecalc(currency, price)
		return per1h, per24h, per7d, vol
		
	def determinerange(self, per1h=None, per24h=None, per7d=None, vol=None, act=None, itemindex=None, mode=None):
		data = []
		changevalues = len(self.changeamt)
		for x in range(0, len(self.exdat) - 1):
			target = self.exdat[x]
			if eval(target) != None:
				buyfactor = int(eval(target))
				for y in range(0, changevalues):
					datindex = y
					if y == 0:
						if buyfactor < self.changeamt[y]:
							
							if self.debugrange:###
								print('Buy factor=' + str(buyfactor) + ' Changeamt=' + str(self.changeamt[y]))
								input()

							break
					if y < changevalues - 2 and y != 0:
						if float(self.changeamt[y]) <= buyfactor and float(self.changeamt[y + 1]) > buyfactor:
							
							if self.debugrange:###
								print('Buy factor=' + str(buyfactor) + ' Changeamt=' + str(self.changeamt[y]))
								input()
								
							break
					if y == changevalues - 1:
						
						if self.debugrange:###
							print('Buy factor=' + str(buyfactor) + ' Changeamt=' + str(self.changeamt[y]))
							input()
							
						break
				if mode == 'buy':
					self.appendexdat(target, act, datindex, itemindex)
				else:
					data.append(datindex)
		if vol != None:
			volfactor = float(vol)
			target = 'vol'
			volvalues = len(self.volumeamt)
			for x in range(0, volvalues):
				datindex = x
				if x == 0:
					if volfactor < float(self.volumeamt[x]):
						break
				if x < volvalues - 2 and x != 0:
					if float(self.volumeamt[x]) <= volfactor and float(self.volumeamt[x + 1]) > volfactor:
						break
				if x == volvalues - 1:
					break
			if mode == 'buy':
				self.appendexdat(target, act, datindex, itemindex)
			else:
				data.append(datindex)
		return data
	def appendexdat(self, target, act, datindex, itemindex):
		if act == '.pop(':
			com = 'self.' + target + act + str(itemindex) + ')'
			res = eval(com)
			act2 = '.insert('
			update = 'self.' + target + act2 + str(itemindex) + ', ' + str(datindex) + ')'
			eval(update)
		else:
			com = 'self.' + target + act + str(datindex) + ')'
			eval(com)

	def updatedata(self, currency, puramount, price, per1h, per24h, per7d, vol, found, porindex, index=None, mode=None):
		x = index
		if found:
			self.holdingswait[x] = self.basewait * self.usddisburse##
			self.holdingsamt[x] = Decimal(self.holdingsamt[x]) + Decimal(puramount)
			self.buyportion[x] = porindex
			self.buyprice[x] = price
			act = '.pop('
		else:
			self.holdingswait.append(self.basewait)
			self.holdingsname.append(currency)
			self.holdingsamt.append(puramount)
			self.buyprice.append(price)
			self.points.holdingsname.append(self.basepts)
			self.buyportion.append(porindex)
			act = '.append('
		self.determinerange(per1h, per24h, per7d, vol, act, index, mode)
		self.curdata.append(str(puramount) + ':' + currency)
			
	def selloff(self, mode=None):
		cooldown = 0
		print('Seems I made some decent profits... sell all the things!')
		self.selloffcnt = self.selloffcnt + 1
		for x in range(0, len(self.holdingsname)):
			if x != 0 and x != 1:
				price = self.pulldata('price_btc', self.holdingsname[x], self.curturn, 'one')
				thresh = Decimal(self.buyprice[x]) * Decimal(self.sellthresh) * Decimal(self.sellfactor)
				comp = 'price > thresh'
				if mode == 'sellthresh':
					sellpoint = self.buyprice[x] - self.buyprice[x] * Decimal(self.sellfactor)
					thresh = self.buyprice[x] + sellpoint
					comp = 'price < thresh'
				if eval(comp):
					sellamount = Decimal(self.holdingsamt[x])
					sellval = Decimal(sellamount) * Decimal(price)
					if sellval >= Decimal(0.002):
						self.calcfees(sellamount, price, self.holdingsname[x])
						fee = Decimal(sellval) * Decimal(self.basefee)
						sellval = Decimal(sellval) - Decimal(fee)
						#######################
						self.correward(x, self.buyprice[x], price)
						self.holdingsamt[0] = Decimal(self.holdingsamt[0]) + Decimal(sellval)
						self.holdingsamt[x] = 0
						cooldown += self.cooldownfactor
						curind = self.currency.index(self.holdingsname[x])
						reducebuyfactor = self.points.currency[curind] * Decimal(1.5) - self.usddisburse
						self.points.currency[x] = reducebuyfactor
						price = Decimal(price)
						self.rewardexdat(x, price)##############################################
						self.correward(x, self.buyprice[x], price)
		usdratio = self.usddisburse * self.usd_val				
		if mode != 'sellthresh':
			if self.holdingsamt[1] > usdratio:
				cooldown = self.selloffprimary(mode, usdratio, cooldown)

		if self.holdingsamt[1] < usdratio:
			cooldown = self.selloffprimary(mode, usdratio, cooldown)
		
		self.cooldown += cooldown
				
	def selloffprimary(self, mode, usdratio, cooldown):
		### Defines special rules for selloffs involving bitcoin and usd
		usdpor = self.holdingsamt[1] - usdratio
		
		if mode != 'sellthresh':
			if usdpor > 0:
				currency, price, portionbase, porindex = self.prepbuysell(None, 'check', 'usd')
				sellval = usdpor * price
				if sellval > 0.002:
					thresh = Decimal(self.buyprice[1]) * Decimal(self.sellthresh) * Decimal(self.sellfactor)
					if price >= thresh:
						self.calcfees(self.holdingsamt[1], price, 'usd')
						fee = Decimal(sellval) * Decimal(self.basefee)
						sellval = sellval - fee
						self.holdingsamt[1] -= usdpor
						currency, price, portionbase, porindex = self.prepbuysell(None, 'sellthresh', 'bitcoin')
						self.holdingsamt[0] = self.holdingsamt[0] + sellval
						cooldown += self.cooldownfactor
		if mode == 'sellthresh':
			if usdpor < 0:
				usdpor = abs(usdpor)
				currency, price, portionbase, porindex = self.prepbuysell(None, 'check', 'bitcoin')
				sellamt = usdpor / price
				if sellamt > 0.002:
					sellpoint = self.buyprice[0] - self.buyprice[0] * Decimal(self.sellfactor)
					thresh = self.buyprice[0] + sellpoint
					if price <= thresh:
						sellval = sellamt * price
						self.calcfees(sellamt, price, 'bitcoin')
						fee = Decimal(sellval) * Decimal(self.basefee)
						sellval = sellval - fee
						self.holdingsamt[0] -= sellamt
						currency, price, portionbase, porindex = self.prepbuysell(None, 'sellthresh', 'usd')
						self.holdingsamt[1] += sellval			
						cooldown += self.cooldownfactor
						
		return cooldown
			
	def sell(self, mode=None, currency=None):
		getcontext().prec = self.preci
		action = 'sellportion'
		btcusd = False
		sellpass = False
		
		if mode == None:
			currency = self.rollchoice('holdingsname')
			self.curattrib[0] = currency
		if currency == 'bitcoin' or currency == 'usd':
			btcusd = True
		currency, price, portionbase, porindex = self.prepbuysell(action, mode, currency)

		if len(self.holdingsname) > 2:
			x = self.holdingsname.index(currency)
			if self.holdingsamt[x] > 0:
				thresh = Decimal(self.buyprice[x]) * Decimal(self.sellthresh) - Decimal(self.buyprice[x])
				highthresh = Decimal(self.buyprice[x]) + Decimal(thresh)
				lowthresh =  Decimal(self.buyprice[x]) - Decimal(self.buyprice[x]) * Decimal(self.lowthreshfactor)
				if price >= highthresh:
					sellpass = True
				if price <= lowthresh:
					sellpass = True
				if mode == 'basic':
					sellpass = True
				if btcusd:
					sellpass = True
				if sellpass:
					sellamount = Decimal(self.holdingsamt[x]) * Decimal(portionbase)
					sellval = Decimal(sellamount) * Decimal(price)
					
					minimum = Decimal(self.sellminimum)
					if currency == 'bitcoin':
						minimum = minimum * Decimal(self.pulldata('price_usd', 'bitcoin'))
					######################################################
					### Sell at least minimum amount, if not then stop ###
					######################################################
					if sellval < minimum:
						while True:
							try:
								porindex = porindex + 1
								portionbase = self.portion[porindex]
								sellamount = Decimal(self.holdingsamt[x]) * Decimal(portionbase)
								sellval = Decimal(sellamount) * Decimal(price)
								if sellval >= (minimum):
									break
							except IndexError:
								print("Tried to sell, but I don't possess the minimum!")
								if mode == None:
									self.curdata.append('None')
								return None
					#######################################################
					
					################################################################################
					### Make sure at least minimum sell amount of coin would be left before sell ###
					################################################################################
					if self.maxusdstrat:
						if currency == 'bitcoin':
							if sellval + self.holdingsamt[1] > self.usddisburse * self.usd_val:
								print('I wanted to sell bitcoin, but I dont want too much cash on hand!')
								if mode == None:
									self.curdata.append('None')
								return None
							if self.disburse < self.maxdisburse:
								print('I wanted to sell bitcoin, but I need to check out other currencies too')
								self.disburse = self.disburse + self.disbursegain
								if mode == None:
									self.curdata.append('None')
								return None
					if portionbase != '1':
						resultamt = Decimal(self.holdingsamt[x]) - Decimal(sellamount)
						valueremain = Decimal(resultamt) * Decimal(price)
						if valueremain < Decimal(self.minimumremain):
							print('I wanted to sell, had enough to sell, but it would leave me with unsellable amount left!')
							if mode == None:
								self.curdata.append('None')
							return None
					#######################
					### Adjust for fees ###
					#######################
					self.calcfees(sellamount, price, currency)
					fee = Decimal(sellval) * Decimal(self.basefee)
					sellval = Decimal(sellval) - Decimal(fee)
					#######################
					self.rewardexdat(x, price)##############################################
					self.correward(x, self.buyprice[x], price)
					ohind = 0
					if currency == 'bitcoin':
						ohind = 1
					self.holdingsamt[ohind] = Decimal(self.holdingsamt[ohind]) + Decimal(sellval)
					self.holdingsamt[x] = Decimal(self.holdingsamt[x]) - Decimal(sellamount)
					datap = 'self.curdata.append((' + str(sellamount) + ', "' + currency + '"))'
					if mode == 'perform':
						self.points.currency[x] = Decimal(self.points.currency[x]) - Decimal(self.basepenalty)
					if mode == None:
						eval(datap)
				
				else:
					print('Wanted to sell, but the price isnt looking good.')
					if mode == None:
						self.curdata.append('None')
			else:
				print('Wanted to sell, but I dont have any of that currency!')
				if mode == None:
					self.curdata.append('None')
		else:
			print('Decided to sell, but have nothing to sell!')
			if mode == None:
				self.curdata.append('None')
		
	def rewardexdat(self, index, price):
		change = price / self.buyprice[index] * 100 - 100
		for x in range(0, len(self.exdat)):
			dpt = self.exdat[x]
			scindex = eval('self.' + dpt + '[' + str(index) + ']')
			scpt = self.changeref[x]
			
			curpts = eval('self.points.' + scpt + '.pop(' + str(scindex) + ')')
			amendpts = change * self.exdatbasepts + Decimal(curpts)
			eval('self.points.' + scpt + '.insert(' + str(scindex) + ', ' + str(amendpts) + ')')
			
			
	def output(self, cyc=0):### analyze and calc different? or included in both? ##
		self.curattrib.append('None')
		comp1 = ''
		index1 = ''
		comp2 = ''
		index2 = ''
		for y in range(0, len(self.curact)):
			if self.curact[y] == 'operand':
				opindex = y
		op = self.curattrib[opindex]
		oploc = self.operand.index(op)
		if oploc < 4:
			mode = 'calc'
		else:
			mode = 'compare'
		for y in range(0, len(self.curdata)):
			x = y + self.turnlength
			if 'dpts' in self.curact[x]:
				if cyc == 0:
					comp1 = self.curdata[x]
					index1 = x
				if cyc == 1:
					comp2 = self.curdata[x]
					index2 = x
				cyc = cyc + 1
				if cyc == 2:
					break
		check = 'Decimal(comp1) ' + op + ' Decimal(comp2)'
		try:
			output = eval(check)
		except:
			print('Error: Division by zero?')
			output = False
		return output
			
	def wait(self):
		self.curturn = self.curturn + 1
		self.turnlength = len(self.curact)
		self.waitbool = True
		self.curdata.append('None')
		
	def start(self, clist):###
		self.populatecurrency(clist)
		self.populatescores()
		
	def portionbonus(self, bvalue, currency):
		sevenday = self.pulldata('perchange_7d', currency)
		data = self.determinerange(per7d=sevenday)
		factor = data[0]
		if factor == 0:
			factor = 1
		bvalue *= factor
		return bvalue
		
	def rollportion(self, action, currency, mode):
		start = 0
		cpool = 0
		choices = []
		decided = False
		
		for x in range(0, len(self.portion)):
			scorecom = 'self.points.' + action + '[x]'
			bvalue = eval(scorecom)
			actvalue = bvalue + self.corbonus(action, bvalue)
			actvalue = int(self.portionbonus(actvalue, currency))
			
			end = actvalue + start
			drange = (start, end)
			choices.append(drange)
			cpool = cpool + actvalue
			start = end
			
		choice = random.randint(0, cpool)
		if choice == cpool:
			choice = choice - 1
		for x in range(0, len(choices)):
			chrange = choices[x]
			if choice in range(chrange[0], chrange[1]):
				decided = True
				decision = self.portion[x]
				break
		if not decided:
			if self.indecisionpause:
				print('[Proportions] :: System failed to make a decision:')
				print('Choice = ' + str(choice) + '\nChoices = ' + str(choices))
				input()
		return decision, x
	
	def nonzeropts(self):#not in use
			##########################################
			### refresh points so no choice hits 0 ###
			##########################################
			pointlist = eval('self.points.' + str(category))
			if any(pointlist) <= self.baserestore:
				for x in range(0, len(pointlist)):
					if pointlist[x] <= self.baserestore:
						pointlist[x] = self.baserestore
			###########################################
	
	def rollchoice(self, category):
		checkcur = False
		decided = False
		print('Making a choice for ' + category)
		start = 0
		cpool = 0
		choices = []
		if self.disburse >= self.maxdisburse:
			self.primed = True
		if category == 'dpts2':
			category = 'dpts'
		lsattrib = []
		targetcategory = eval('self.' + category)
		for x in range(0, len(targetcategory)):
			lsattrib.append(targetcategory[x])
		choicevals = []
		for x in range(0, len(lsattrib)):

			attribute = eval('self.' + category + '[x]')
			
			scorecom = 'self.points.' + str(category) + '[x]'
			bvalue = eval(scorecom)
					
				##################################################
				### Adjust to intelligently sell/buy BTC & USD ###
				##################################################
			if category == 'holdingsname':
				if self.btcusdintelstrat:
					if self.primed:
						if x == 0 or x == 1:
							currency = self.holdingsname[x]
							currency, price, portionbase, porindex = self.prepbuysell(None, 'check', currency)
							val = self.holdingsamt[x]
							if x == 1:
								val = self.holdingsamt[x] * price
							if self.buyprice[x] > price:
								factor = self.buyprice[x] / price * self.btcusdfactor
								bvalue = bvalue * factor
							if self.buyprice[x] < price:
								factor = price / self.buyprice[x] * self.btcusdfactor
								bvalue = bvalue * factor
				###################################################
			if bvalue <= 0:
				bvalue = 1
				
			cordecide = False
			if self.correlationstrat:
				if category == 'action':
					actvalue = bvalue + self.correlatedecide(attribute, bvalue)
					cordecide = True
			
			if not cordecide:
				actvalue = bvalue + self.corbonus(attribute, bvalue)
			if category == 'currency':
				actvalue = Decimal(actvalue) + Decimal(self.exdatbonus(attribute, actvalue))
					
			if self.disbursestrat:
				if attribute == 'buy':
					if self.disburse < self.preferbuy:
						bvalue = self.preferbuyset
						self.prebuyactive = True
					else:
						self.prebuyactive = False
						
			if self.targetusdstrat:
				checkadj = False
				if 1 == 1:#self.primed:

					
					
					
					if category == 'holdingsname':# Applies only to Selling
						if x == 0 or x == 1:#Applies only to Selling Bitcoin/USD, ensures useles calcs arent made when checking other OH currencies

							actvalue = Decimal(actvalue)
							usddfac = self.targetusdfactor + 1
							pricebtc = self.pulldata('price_usd', 'bitcoin')
							
							
							usdcomphigh = self.usd_val * self.usddisburse * usddfac
							usdconv = self.usd_val * self.usddisburse * self.targetusdfactor
							usdcomplow = self.usd_val * self.usddisburse - usdconv		
							
							usd2btc = Decimal(1) / Decimal(pricebtc) * self.holdingsamt[1] #BTC value of current USD holdings
							checkadjust = False
							info = ''
							print('Before modification decision value: ' + str(actvalue))
							if self.holdingsamt[1] < usdcomplow: # Check USD amount vs. Low Comparison value
								if x == 0:#For bitcoin:
									if self.holdingsamt[0] > 0.002: #Check to make sure amt of bitcoin > Minimum transaction amount
										info += 'Too little USD, increasing odds of selling BTC. '
										actvalue *= self.targetusdbonus # Increase odds of selling BTC if USD amt lower than comparison value AND possess atleast minimum BTC
									else:
										if x == 0:
											info = 'Too little usd, and not enough BTC to sell. '
											actvalue = 1 #If not enough bitcoin in possession, reduce odds of trying to sell BTC in order to sell other currency and free up BTC
											#checkadjust = True
								elif x == 1:#For USD:
									info = 'Too little USD already, reducing odds of trying to sell USD.'
									actvalue = 1#Reduce odds of choosing to sell USD if on hand is below target threshhold
							
							elif self.holdingsamt[1] > usdcomphigh:# Check USD amount vs. High Comparison value
								if x == 0:#For bitcoin:
									info = 'Too much USD. Reducing odds of selling BTC.'
									actvalue = 1 #Reduce odds of choosing to sell bitcoin for USD if too much USD on hand
								if x == 1:#For USD:
									if usd2btc > 0.002:# Check to see if usd on hand is enough to sell
										info = 'Too much USD. Increasing odds of selling USD. '
										actvalue *= self.targetusdbonus
									else:
										info = 'Too much USD, but not enough to sell- reducing USD odds in order to aid chance of BTC sales. '
										actvalue = 1
							
							actvalue = int(actvalue)
							if checkadjust:
								self.checkadj('btcsell')
							print('Thinking: ' + info + ' Actual decision value for ' + str(self.holdingsname[x]) + ': ' + str(actvalue))
							#checkcur = True
						
			if checkcur:
				print('Actual decision value for ' + str(self.holdingsname[x]) + ': ' + str(actvalue))

			
			#if attribute == 'wait':
			#	if not self.primed:
			#		actvalue = 1
			
			if attribute == 'buy':
				if not self.primed:
					if x == 0 or x == 1:
						actvalue = 1
		
			if self.doubledownstrat:
				if category == 'currency':
						if lsattrib[x] in self.holdingsname:
							if x != 0 and x != 1:
								if self.primed:
									actvalue *= 2
								else:
									actvalue /= 2
									
			if self.holdingswaitstrat:

				if category == 'holdingsname':
					if self.holdingsname[x] != 'bitcoin' and self.holdingsname[x] != 'usd':
						if self.holdingswait[x] != self.minimumwait:
							factor = Decimal(self.basewait) / self.holdingswait[x]
							actvalue += factor
					else:
						targetusd = self.usddisburse * self.usd_val
						if self.holdingsname[x] == 'usd':
							if self.holdingsamt[1] < targetusd:
								actvalue = 1
							if self.holdingsamt[1] > targetusd:
								actvalue *= self.waitdisbursebonus
						if self.holdingsname[x] == 'bitcoin':
							if self.holdingsamt[1] < targetusd:
								actvalue *= self.waitdisbursebonus
							if self.holdingsamt[1] > targetusd:
								actvalue = 1

				if category == 'action':
						if attribute == 'wait':
							factor = self.usddisburse / Decimal(0.5)
							actvalue = Decimal(actvalue)
							actvalue *= factor
							if self.usddisburse > self.waitdisbursethresh:
								actvalue *= self.waitdisbursebonus
								
						if attribute == 'buy':
							if self.curattrib[0] != 'bitcoin' and self.curattrib[0] != 'usd':
								factor = Decimal(0.5) / self.usddisburse
								actvalue += factor
								if self.usddisburse < self.actdisbursethresh:
									actvalue += self.waitdisbursebonus
						if  attribute == 'sell':
							factor = Decimal(0.5) / self.usddisburse
							actvalue = Decimal(actvalue)
							actvalue += factor
							if self.usddisburse < self.actdisbursethresh:
								actvalue += self.waitdisbursebonus
							
			if category == 'holdingsname':
				if self.holdingsamt[x] == 0:
					actvalue = 1
					
					
					
		####################################
		### Remove < mean valued choices ###
		####################################	
			choicevals.append(actvalue)
		if checkcur:
			print('Considered possibilities: ' + str(lsattrib))
			print('With values: ' + str(choicevals))
		total = 0
		chvalls = len(choicevals)
		for x in range(0, chvalls):
			total += int(choicevals[x])
		avgval = Decimal(total) / Decimal(chvalls)
		
		poplist = []
		popvalues = []
		popind = []
		if category == 'currency' or category == 'holdingsname':
			for x in range(0, chvalls):
				if self.primed:
					if choicevals[x] < avgval * self.avgvalfactor:
						
						popvalues.append(choicevals[x])
						poplist.append(lsattrib[x])
						popind.append(x)
						if checkcur:
							print('Decided to pop ' + str(lsattrib[x]) + ' from the list. Avgval= ' + str(avgval) + ' Choicevalue= ' + str(choicevals[x]))
			if checkcur:
				print('Poplist: ' + str(poplist))
			adjustindex = 0
			psize = len(poplist)
			if psize == len(lsattrib):
				psize -= 1
			for x in range(0, psize):
				target = min(popvalues)
				ind = popvalues.index(target)
				taratrib = poplist[ind]
					
				popvalues.pop(ind)
				poplist.pop(ind)
				choicevals.remove(target)
				lsattrib.remove(taratrib)
				
			
		for x in range(0, len(choicevals)):
		#####################################
			actval = choicevals[x]
			end = int(actvalue + start)
			drange = (start, end)
			choices.append(drange)
			cpool = int(cpool + actvalue)
			start = int(end)
			
		choice = random.randint(0, cpool)
		if choice == cpool and choice != 0:
			choice = choice - 1
		if checkcur:
			print('Current choicepool: ' + str(cpool))
			print('All current holdings knowledge: ' + str(self.holdingsname) + '\n')
			print('All current possible attributes: ' + str(lsattrib) + '\n')
			for x in range(0, len(choices)):
				print(str(lsattrib[x]) + ' Choice value range: ' + str(choices[x]))
			print('Choice value= ' + str(choice))
			
		for x in range(0, len(choices)):
			chrange = choices[x]
			if int(choice) in range(chrange[0], chrange[1]):
				decision = lsattrib[x]
				decided = True
				break
		if checkcur:
			print('Decision= ' + str(decision))
			input()
		if not decided:
			if len(choices) == 1:
				decision = lsattrib[0]
				decided = True
			if self.indecisionpause:
				if not decided:
					print('[Attribute Choices] :: System failed to make a decision:')
					print('Choice = ' + str(choice) + '\nChoices = ' + str(choices))
					input()
		print('Decided on ' + str(decision))
		if decision == 'buy':
			self.cooldown += self.cooldownfactor
			self.points.action[0] -= self.usddisburse * self.buyreductionfactor### or -= 1
			if self.points.action[0] < 1:
				self.points.action[0] = 1
		return decision
		
	def checkadj(self, mode):
		usdval = Decimal(self.btc_profval) / Decimal(self.usd_val)
		usdval *= Decimal(self.holdingsamt[1])
		targetval = self.btc_profval * self.targetusdfactor
		if mode == 'btcsell':
			if self.holdingsamt[0] < targetval:
				growrange = []
				growindex = []
				shrinkrange = []
				shrinkindex = []
				highgrow = False
				found = False
				for x in range(0, len(self.holdingsname)):
					if x != 0 and x != 1:
						if self.holdingsamt[x] != 0:
							currency = self.holdingsname[x]
							cprice = self.pulldata('price_btc', currency)
							bprice = self.buyprice[x]
							growth = Decimal(cprice) / Decimal(bprice)
							if growth > self.growthfactor:
								highgrow = True
								growrange.append(growth)
								growindex.append(x)
							shrinkrange.append(growth)
							shrinkindex.append(x)
							found = True
				if found:
					if highgrow:
						target = max(growrange)
						growind = growrange.index(target)
						curind = growindex[growind]
					else:
						target = min(shrinkrange)
						shrinkind = shrinkrange.index(target)
						curind = shrinkindex[shrinkind]
					currency = self.holdingsname[curind]
					self.sell('basic', currency)
				
		
	def exdatbonus(self, currency, bvalue):
		if currency != 'bitcoin' and currency != 'usd':
			curindex = self.currency.index(currency)
			per1h, per24h, per7d, vol = self.pullexdat(currency)
			data = self.determinerange(per1h, per24h, per7d, vol, None, None, 'bonus')
			bonus = 0
			pts = 0
			for x in range(0, len(self.exdat)):
				
				item = self.changeref[x]
				pointlist = eval('self.points.' + item)
				pointindex = data[x]
				pts = Decimal(pts) + Decimal(pointlist[pointindex])
			result = pts * self.exdatbasepts
			if result < self.exdatreference:
				if self.predictsell:
					if currency in self.holdingsname:
						curind = self.holdingsname.index(currency)
						if self.holdingsamt[curind] > 0:
							print('Found a low performing currency Im holding, trying to sell. Pts = ' + str(result))
							self.sell('perform', currency)
			if result < 0:
				result = 1
			return result
		else:
			return 1
		
		
	def getrecentcur(self):
		catcopy = self.curact.copy()
		curcopy = self.curattrib.copy()
		catcopy.reverse()
		curcopy.reverse()
		curloc = catcopy.index('currency')
		currency = curcopy[curloc]
		return currency
			
	def playturn(self, mode='norm'):
		getcontext().prec = self.preci
		print('Current turn: ' + str(self.curturn))
		for x in range(0, len(self.cats) - 1):
			cat = self.cats[x]
			self.curact.append(cat)
			if cat != 'output' and cat != 'action':
				attribute = self.rollchoice(cat) ### need to grab data for currency, 
				self.curattrib.append(attribute)
				if 'dpts' in cat:
					currency = self.getrecentcur()
					data = self.pulldata(attribute, currency, self.curturn, 'one')
					self.curdata.append(data)
				else:
					self.curdata.append('None')
			if cat == 'output':
				if self.outputcalc:
					result = self.output(0) ###
					self.curdata.append(result)
				else:
					self.curattrib.append('Null')
					self.curdata.append('Null')
			if cat == 'action':
				attribute = self.rollchoice(cat)
				self.curattrib.append(attribute)
				actcom = 'self.' + attribute + '()'
				eval(actcom)
			if self.debug:
				print()
				for z in range(0, len(self.turncats)):
					tcat = self.turncats[z]
					turncatlist = eval('self.' + tcat)
					info = 'Turn Category: ' + tcat + ' Length: '
					try:
						info = info + str(len(turncatlist))
					except TypeError:
						None
					print(info)
					print(str(turncatlist))
			self.consoleoutput()
			
		self.rewards()
		##########################
		### Threshhold sellout ### Experimental
		##########################
		sellthresh, lowthresh = self.sthresh()
		if self.selloffstrat:
			if self.btc_profval > sellthresh or self.btc_profval <= lowthresh:
				if self.btc_profval <= lowthresh:
					self.selloff('sellthresh')
				else:
					self.selloff()
				self.threshval = self.btc_profval
		##########################

		self.endturn()
		
	def consoleoutput(self):
		os.system('clear')
		info = ''
		for x in range(0, len(self.holdingsname)):
			cur = self.holdingsname[x]
			amt = self.holdingsamt[x]
			if amt > 0:
				info = info + cur + ':' + str(amt) + '; '
		getcontext().prec = 4
		sellthresh, lowthresh = self.sthresh()
		targetusd = float(self.usd_val * self.usddisburse)
		print('Portfolio: ' + info + '\n')
		print('Current portfolio value:\n(USD)$' + str(self.usd_val) + '\t(BTC)' + str(self.btc_profval) + '\t Fees paid: ' + str(self.feespaid) + '(BTC) ' + '\t Transactions: ' + str(self.transactions) + '\n\nDisbursement: ' + str(self.disburse) + '\tPrebuy: ' + str(self.prebuyactive))
		print('Currency range: ' + str(len(self.currency)) + '\n Target USD Holding: ' + str(targetusd) + '\t USD Disburse: ' + str(self.usddisburse))
		print('High Sell threshold: ' + str(sellthresh) + '\tLow Sell threshold: ' + str(lowthresh) + '\tSelloff Count: ' + str(self.selloffcnt) + '\n')
		print('Turn number:\t' + str(self.curturn) + ' Primed: ' + str(self.primed) + '\n')
		if self.finetuning:
			print('Finetuning Enabled.\nEstimated time remaining: ' + str(self.fttimeremain) + '\n\nTesting Attribute: "' + str(self.ftattrib) + '" for variables: ' + str(self.ftallvars) + '. Current test variable: ' + str(self.ftvar) + '\n')
			print('Finetune info:\nCurrent trial:\tCurrent run:\tTotal runs:\t\tAvg. Turn Time:\t\t\tEst. Run Time:')
			print(str(self.fttrial) + '\t\t' + str(self.ftturn) + '\t\t' + str(self.fttotal) + '\t\t\t' + str(self.ftturntime) + '\t' + str(self.fttesttime) + '\n')
			print('Current stats:\nAverage BTC:\tAverage USD:\t\tMin BTC:\tMin USD:\tMax BTC:\tMax USD:')
			print(str(self.ftavgbtc) + '%\t\t' + str(self.ftavgusd) + '%\t\t\t' + str(self.ftmlossbtc) + '%\t' + str(self.ftmlossusd) + '%\t' + str(self.ftmgainbtc) + '\t\t' + str(self.ftmgainusd))
			print('Gain runs: ' + str(self.ftrungain) + ' Loss runs: ' + str(self.ftrunloss) + ' Fail Rate: ' + str(self.ftfailrate) + '% Average Fail Loss: ' + str(self.ftavgfailloss) + '\n\n')
			
	def sthresh(self):
		sellthresh = Decimal(self.threshval) * Decimal(self.sellthresh)
		lowthresh = sellthresh - Decimal(self.threshval) * Decimal(self.sthreshfactor)
		return sellthresh, lowthresh
		
	def endturn(self, cont=True):
		print('Ending turn: ' + str(self.curturn))
		turncalc = self.turnfreq + self.cooldown
		waitfactor = Decimal(0.5) / self.usddisburse
		self.curturn += turncalc
		for x in range(0, len(self.holdingswait)):
			if self.holdingswait[x] > turncalc * waitfactor + self.minimumwait:
				self.holdingswait[x] -= turncalc * waitfactor
			else:
				self.holdingswait[x] == self.minimumwait
		self.cooldown = 0
		self.turnlength = 0
		if self.masterinfo:
			self.dataoutput()
		for x in range(0, len(self.turncats) - 1):
			com = 'self.' + self.turncats[x] + '.clear()'
			eval(com)
	
	def updatemaxusd(self):
		if self.usddisbursestrat:
			aph = 30 / self.turnfreq
			factors = (1, 24, 168)
			factind = self.exdat.index(self.changeduration)
			changefactor = factors[factind] * aph
			flation = self.initbtcprice / self.pulldata('price_usd', 'bitcoin')
			
			
			if self.disburse >= self.maxdisburse:
				per1h, per24h, per7d, vol = self.pullexdat('bitcoin')
				disbursechg = Decimal(eval(self.changeduration)) * Decimal(self.usddisburse) / 100 * -1
				self.usddisburse = self.usddisburse + disbursechg / Decimal(changefactor) * self.usddisbursechangerate
				
			if self.usddisburse > 1 or self.usddisburse < self.usdminimumdisburse:
				if self.usddisburse > 1:
					self.usddisburse = 1
				if self.usddisburse < self.usdminimumdisburse:
					self.usddisburse = self.usdminimumdisburse

	def rewards(self):
		getcontext().prec = self.preci
		print('Calculating rewards...')

		self.updatemaxusd()
		
		basereward = self.basereward
		btc_price = self.pulldata('price_usd', 'bitcoin', self.curturn + 1, 'one')
		value, btcvalue = self.result()
		#######################
		### get change in % ###
		#######################
		proportion = Decimal(value) / Decimal(self.usd_val) * Decimal(100.0) - Decimal(100.0)
		proportionbtc = Decimal(btcvalue) / Decimal(self.btc_profval) * Decimal(100.0) - Decimal(100.0)
		#######################
		
		###############################
		### calc point value reward ###
		###############################
		change = Decimal(basereward) / Decimal(100.0) * Decimal(proportion)
		changebtc = Decimal(basereward) / Decimal(100.0) * Decimal(proportionbtc)
		###############################
		
		#########################
		## Experinmental mods ###
		#########################
		
		if changebtc > self.learningthresh:
			if change < changebtc:
				#input()
				change = changebtc * self.gainfactor
		else:
			change *= self.lossfactor
			change += self.lossadjust
		#########################
		
		##########################
		### Selloff adjustment ### Experimental
		##########################
		thresh = Decimal(self.threshval) * Decimal(self.sellthresh) - Decimal(self.threshval)
		testthresh = Decimal(self.threshval) - thresh * 2 ##
		if btcvalue < testthresh:
			self.threshval = btcvalue
		##########################
		##########################
		self.usd_val = value
		self.btc_profval = btcvalue
		for x in range(0, len(self.curact)):
			cat = self.curact[x]
			if cat != 'output':
				attrib = self.curattrib[x]
				data = self.curdata[x]
				if cat == 'dpts2':
					cat = 'dpts' 
				findindex = 'self.' + cat + '.index("' + attrib + '")'
				ptindex = eval(findindex)
				findpts = 'self.points.' + cat + '.pop(' + str(ptindex) + ')'
				curpts = eval(findpts)
				adjpts = Decimal(curpts) + Decimal(change)
				adjpts = int(adjpts)
				insertpts = 'self.points.' + cat + '.insert(' + str(ptindex) + ', ' + str(adjpts) + ')'
				eval(insertpts)
		
			if self.sellfactorstrat:
				if self.curattrib[x] == 'sell':
					info = self.curdata[x]
					if info != 'None':
						cur = info[1]
						for x in range(0, len(self.holdingsname)):
							if self.holdingsname[x] == cur:
								curpts = Decimal(self.points.holdingsname[x])
								adjpts = Decimal(curpts) + Decimal(change)
								self.points.holdingsname[x] = Decimal(adjpts)
					
	def percentreward(self, target, y):
		findpts = 'self.points.' + target + '.pop(' + str(y) + ')'
		curpts = eval(findpts)
		adjpts = curpts + change
		insetpts = 'self.points.' + target + '.insert(' + str(y) + ', ' + str(adjpts) + ')'	
		return True
						
		#for x in range(0, len(self.holdingsname)):
			

	def result(self):
		getcontext().prec = self.preci
		btcvalue = 0
		for x in range(0, len(self.holdingsname)):
			currency = self.holdingsname[x]
			if currency != 'usd' and currency != 'bitcoin':
				quan = Decimal(self.holdingsamt[x])
				price = self.pulldata('price_btc', currency, self.curturn + 1, 'one')
				value = Decimal(price) * Decimal(quan)
				btcvalue = btcvalue + value
			if currency == 'usd':
				quan = Decimal(self.holdingsamt[x])
				price = 1 / Decimal(self.pulldata('price_usd', 'bitcoin', self.curturn + 1, 'one'))
				value = Decimal(price) * Decimal(quan)
				btcvalue = btcvalue + value
		btcvalue = Decimal(btcvalue) + Decimal(self.holdingsamt[0])
		btcusd_value = self.pulldata('price_usd', 'bitcoin', self.curturn + 1, 'one')
		usd_value = Decimal(btcvalue) * Decimal(btcusd_value)
		self.curturn = self.curturn + 1
		#if usd_value < 10:
		#	self.endgame()
		return usd_value, btcvalue
			
	def corbonus(self, attribute, bvalue):
		if self.correlationstrat:
			return bvalue
		bonus = 0
		if len(self.correlate) > 0:
			futureact = []
			for x in range(0, len(self.curact)):
				futureact.append(self.curact[x])
				futureact.append(attribute)
				correlate = ''.join(futureact)
				for correlate in self.correlate:
					bonus = bonus + 15
					return bonus
		else:
			return bvalue
		
	################################################
	### Report results to initiating system/disk ###
	################################################
	
	def endgame(self):
		info = 'End of game reached. Starting BTC: ' +str(self.starting_btc) + ' Ending BTC: ' + str(self.btc_profval)
		ratiobtc = Decimal(self.btc_profval) / Decimal(self.starting_btc) * 100 - 100
		ratiousd = Decimal(self.usd_val) / Decimal(self.starting_usd) * 100 - 100
		info2 = 'Gain/Loss: ' + str(ratiobtc) + '(BTC) ' + str(ratiousd) + '(USD)'
		print(info)
		print(info2)
		with open('finalresuls.list', 'a+') as out:
			out.write(info)
			out.write('\n')
			out.write(info2)
		if self.persistence:
			self.savedata()
		
	def calldata(self):
		ratiobtc = Decimal(self.btc_profval) / Decimal(self.starting_btc) * 100 - 100
		ratiousd = Decimal(self.usd_val) / Decimal(self.starting_usd) * 100 - 100
		return ratiousd, ratiobtc
		

	def dataoutput(self):
		if self.dataoutputon:
			print(str(len(self.points.correlate1)))
			print(str(len(self.correlate1)))
			with open('datascores.out', 'a+') as out:
				out.write('Data for turn: ' + str(self.curturn) + '\n')
				out.write('Turn Actions taken: ' + str(self.curact) + '\n')
				out.write('Turn Action Attributes: ' + str(self.curattrib) + '\n')
				out.write('Turn Action Attribute Data: ' + str(self.curdata) + '\n')
					
				for x in range(0, len(self.points.relist)):
					item = self.points.relist[x]
					scorelist = eval('self.points.' + item)
					out.write('Scores: ' + item + '( Length: ' + str(len(scorelist)))
					out.write('\n')
					for y in range(0, len(scorelist)):
						out.write(str(scorelist[y]))
						out.write(',')
					out.write('\n')
				for x in range(0, len(self.exdat)):
					item = self.exdat[x]
					scorelist = eval('self.' + item)
					out.write('Data: ' + item + '( Length: ' + str(len(scorelist)) + '\n')
					out.write(str(scorelist) + '\n')
				out.write('Data: Holdings: Buy Portion: ' + str(self.buyportion) + '\n')
				out.write('Data: Holdings: Sell Portion: ' + str(self.sellportion) + '\n')
				for x in range(4, len(self.dpts)):
					item = self.dpts[x]
					scorelist = eval('self.points.' + item)
					out.write('Scores: ' + item + '( Length: ' + str(len(scorelist)) + '\n')

					out.write(str(scorelist) + '\n')
				out.write('Scores: Volume_24h Length: ' + str(len(self.points.volume_24h)) + '\n')
				out.write(str(self.points.volume_24h))
				out.write('\nScores: Buy Portion:\n')
				out.write(str(self.points.buyportion))
				out.write('\nScores: Sell Portion:\n')
				out.write(str(self.points.sellportion))
				out.write('\nScores: Holdings Name:\n')
				out.write(str(self.points.holdingsname))
				out.write('\nScores: Holdings Amount:\n')
				out.write(str(self.holdingsamt))
				out.write('\nDecisions: Actions\n')
				out.write(str(self.curact))
				out.write('\nDecisions: Attributes\n')
				out.write(str(self.curattrib))
				out.write('\nDecisions: Data\n')
				out.write(str(self.curdata))
				out.write('\nCurrencies Held:\n')
				for x in range(0, len(self.holdingsname)):
					item = self.holdingsname[x]
					out.write(item + ', ')
				out.write('\nBuy Price:\n')
				out.write(str(self.buyprice))
				out.write('\n\n')
				
