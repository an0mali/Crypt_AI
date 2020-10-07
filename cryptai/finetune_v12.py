import time
from decimal import *
import os
from random import randint
import gc
curver = "12"
vname = "cryptai_v" + curver
com = "import " + vname
exec(com)



class Finetune():
	
	def __init__(self, curver, **kwargs):
		
		
		getcontext().prec = 5
		
		self.trial = False
		self.resultspath = 'finetune.data/avgresults/avgresults_v4.'
		self.configpath = 'finetune.data/config/'
		self.spath = 'finetune.data/system/'
		
		self.vname = "cryptai_v" + curver

		#######################################
		varbool = False
		singletrial = False
		
		self.autotune = False
		self.auto = False
		self.newtune = False
		self.resume = False
		self.prevattrib = False

		self.runs = 250 ##
		
		self.testattrib = 'usd_cur'
		self.testvars = [1000,]
		
		self.autoattribs = ''
		
		if varbool:
			self.testvars = (False, True)
		########################################
		
		clear = False
		self.wait = False
		
		self.timerdy = False
		self.avgtime = ['Not established\t']
		self.estmaxtime = ['Not established\t']
		self.timeremain = ['Not established']
		
		self.turnnum = 0
		self.trialturn = 0
		
		self.info = ('avgusd', 'avgbtc', 'mlossusd', 'mlossbtc')
		self.avgusd = 'No Data'
		self.avgbtc = 'No Data'
		self.mlossusd = 'No Data'
		self.mlossbtc = 'No Data'
		self.mgainusd = 'No Data'
		self.mgainbtc = 'No Data'
		self.avgfailloss = 0
		
		self.failloses = []
		
		self.runloss = 0
		self.rungain = 0
		self.failrate = 0
		
		self.accuracy = 100 / self.runs
		
		self.saveitems = ('tunedattribs', 'tunedvalues')
		self.tunedattribs = []
		self.tunedvalues = []
		self.tunedtimes = []
		self.relativescore = []
		
		self.bestval = []
		self.bestscore = []
		
		
		self.totalruns = 0

		
		self.stop = len(self.testvars)
		if singletrial:
			self.stop = 1
		if self.trial:
			self.stop = 1
			self.runs = 2
		
		if clear:
			with open('avgresults.' + self.testattrib, 'w+') as clear:
				clear.write('')
				
		self.waittime = 3
		print('Configure testing module?')
		config = self.yesno()
		
		auto = False
		if config:
			self.setup()
			self.totalruns = self.runs * len(self.testvars)
			self.stop = len(self.testvars)
		else:
			print('Enable autotune function?')
			self.auto = self.yesno()
		
		##################################
		### Basic startup logic checks ###
		##################################	
		checkres = self.systemchecks()
		
		if not config:	
			if 'finetune.resume' in checkres:
				print('Previous session detected. Would you like to resume?')
				self.resume = self.yesno()
				if self.resume:
					os.system('cp vars.curattrib prev.attrib')
					self.prevattrib = True
				
		if not self.resume:
			if 'tuned.autotune' in checkres:
				try:
					os.system('mv tuned.autotune tuned.autotune_bkup')
				except:
					None
			if 'prev.attrib' in checkres:
				print('Previous variables file detected. Would you like to load?')
				self.prevattrib = self.yesno()
				
		if not self.resume:
			if not self.auto:
				self.start()
			else:
				self.runautotune()
		else:
			self.runautotune(resume=True)

		##################################
		
	class results(object):
		totalusd = 0
		totalbtc = 0
		rusd = []
		rbtc = []
		
		turntime = []
		
	def systemchecks(self):
		checkres = os.listdir()
		reqdirs = ('finetune.data', 'avgresults', 'config', 'system')
		### Try to create system directories
		for x in range(0, len(reqdirs)):
			try:
				if x == 0:
					os.system('mkdir -p ' + reqdirs[x])
				else:
					os.system('mkdir -p ' + reqdirs[0] + '/' + reqdirs[x])
			except:
				None
			
		return checkres
		
	def runautotune(self,resume=False):

			print('Initializing variables...')
			attribs, startvals, variances = self.loadtestattribs()
			if not resume:
				self.customruns()
			escape = False
			if attribs != 'fail':
				for x in range(0, len(attribs)):
					if resume:
						with open('finetune.resume', 'r') as dat:
							for line in dat:
								line = line.strip()
								start = 0
								end = line.find('=')
								var = line[start:end]
								if var == 'attrib':
									start = end + 1
									end = line.find(';;')
									val = line[start:end]
									break
						#try:
						#	skip = attribs.index(val)
						#	if x == skip
						#		continue
						#except IndexError:
						#	None
						resume = False
					if not escape:
						attrib = attribs[x]
						startval = startvals[x]
						variance = variances[x]
						escape = self.autotunerun(attrib, startval, variance, resume)
			else:
				print('Error loading test attributes. Aborting.')
				
			if escape:
				print('Processes interrupted by user. Current status saved.')
		
	def yesno(self):
		answers = ('y', 'Y', 'n', 'N')
		while True:
			res = input('Enter Y for yes or N for no: ')
			if res in answers:
				break
			else:
				print('Select a valid response.')
					
		sel = answers.index(res)
		if sel == 0 or sel == 1:
			return True
		else:
			return False
			
	def askattrib(self):
		
		while True:
			attrib = input('Enter target test attribute: ')
			print('Attribute: "' + attrib + '". Is this correct?')
			cont = self.yesno()
			if cont:
				self.testattrib = attrib
				break
				
	def askbool(self):
		
		while True:
			print('Is this a boolean test?')
			cont = self.yesno()
			if cont:
				self.testvars = (False, True)
				boolean = True
				break
			else:
				boolean = False
				break
		return boolean
		
	def asksingletrial(self):

		while True:
			print('Enable single trial?')
			cont = self.yesno()
			if cont:
				single = True
				break
			else:
				single = False
				break
		return single
		
	def intestvars(self):
		testvars = []
		while True:
			while True:
				try:
					var = input('Enter test attributes. Press ctrl + c when done.')
					testvars.append(var)
				except KeyboardInterrupt:
					break
			print('Test atrributes: ' + str(testvars) + '. Is this correct?')
			cont = self.yesno()
			if cont:
				break
			else:
				testvars = []
		return testvars
		
	def addtestvars(self, testvars):

		self.varbool = False
		self.testvars = []
		for x in range(0, len(testvars)):
			try:
				self.testvars.append(float(testvars[x]))
			except TypeError:
				self.testvars.append(testvars[x])
				
	def customruns(self):
		
		print('Default runs set to ' + str(self.runs) + '. Enter custom number of runs?')
		cont = self.yesno()
		if cont:
			while True:
				try:
					runs = int(input('Enter number of runs: '))
					print('Number of runs set to ' + str(runs) + '. Is this correct?')
					cont = self.yesno()
					if cont:
						break
					else:
						continue
				except TypeError:
					print('Entry must be a nummber.')
			self.runs = runs
			self.totalruns = self.runs * len(self.testvars)
				
	def setup(self):
		self.askattrib()
		
		boolean = self.askbool()
		
		if not boolean:
			testvars = self.intestvars()
		
		#single = self.asksingletrial()
		
		if not boolean:
			self.addtestvars(testvars)
		else:
			self.varbool = True
			
		self.customruns()
		
	def loadtestattribs(self):
		lstestattribs = []
		lsbaseval = []
		lsvariance = []
		check = os.listdir()
		if 'testattribs.autotune' in check:
			with open('testattribs.autotune', 'r') as testlist:
				for line in testlist:
					line = line.strip()
					start = 0
					end = line.find(',')
					attrib = line[start:end]
					lstestattribs.append(attrib)
					start = end + 1
					end = line.find(';')
					baseval = line[start:end]
					print(baseval)
					try:
						lsbaseval.append(int(baseval))
					except ValueError:
						
						lsbaseval.append(float(baseval))
					start = end + 1
					end = line.find(';;')
					variance = line[start:end]
					#input(variance)
					lsvariance.append(float(variance))
					
		
			return lstestattribs, lsbaseval, lsvariance
		else:
			print('Error: testattribs.autotune file not found!')
			return 'fail', None, None
			
	def runsim(self, testvar, index):
		getcontext().prec = 5
		attrib = self.testattrib
		com = self.vname + ".Cryptai(" + attrib
		passedvals = [" = testvar, ",
		"ftavgfailloss = str(self.avgfailloss), ",
		"ftfailrate = str(self.failrate), ",
		"ftrungain = str(self.rungain), ",
		"ftrunloss = str(self.runloss), ",
		"ftmgainusd = str(self.mgainusd), "
		"ftmgainbtc = str(self.mgainbtc), ",
		"ftavgusd = str(self.avgusd), ",
		"ftavgbtc = str(self.avgbtc), ",
		"ftmlossbtc = str(self.mlossbtc), ",
		"ftmlossusd = str(self.mlossusd), ",
		"ftturn = str(self.turnnum), ",
		"fttrial = str(index), ",
		"finetuning = True, ",
		"ftvar = str(self.testvars[index]), ",
		"ftturntime = str(self.avgtime[0]), ",
		"ftesttime = str(self.estmaxtime[0]), ",
		"fttotal = str(self.totalruns), ",
		"ftallvars = str(self.testvars), ",
		"ftattrib = str(self.testattrib), ",
		"ftprevattrib = self.prevattrib, ",
		"fttimeremain = str(self.timeremain[0]))"
		]
		
		if self.newtune:
			
			for x in range(0, len(self.tunedattribs)):
				found = False
				item = self.tunedattribs[x] + ' = ' + str(self.tunedvalues[x]) + ', '
				for y in range(0, len(passedvals)):
					if self.tunedattribs[x] in passedvals[y]:
						found = True
						passedvals.pop(y)
						passedvals.insert(y, item)
				if not found:
					passedvals.insert(2, item)
				
		for x in range(0, len(passedvals)):
			com += passedvals[x]
			
		stime = time.time()
		run = eval(com)

		etime = time.time() - stime
		
		ratiousd, ratiobtc = run.calldata()
		run.clearobjs()
		
		print('USD: \t BTC:')
		print(str(ratiousd) + '\t' + str(ratiobtc))
		self.results.rusd.append(Decimal(ratiousd))
		self.results.rbtc.append(Decimal(ratiobtc))
		
		self.results.turntime.append(etime)
		self.timerdy = True
		self.calctimes()
		
	def calctimes(self):
		getcontext().prec = 3
		timeinfo = ('avgtime', 'estmaxtime', 'timeremain')

		if self.timerdy:
			timepassed = 0
			turns = len(self.results.turntime)
			for x in range(0, turns):
				timepassed += Decimal(self.results.turntime[x])
			avgtime = Decimal(timepassed) / Decimal(turns)
			estmaxtime = Decimal(avgtime) * Decimal(self.totalruns)
			avgtimepass = Decimal(avgtime) * Decimal(turns)
			timeremain = Decimal(estmaxtime) - Decimal(avgtimepass)
			
			for x in range(0, len(timeinfo)):
				param = timeinfo[x]
				data = Decimal(eval(param))
				mins = data / 60
				hours = mins / 60
				
				base = 'self.' + param
				com = base + '.pop(0)'
				i = eval(com)
				info = str(mins) + ' (min) / ' + str(hours) + ' (hours)'
				com = base + '.append("' + info + '")'
				eval(com)
			

	def totalturns(self, index):
		total = self.totalruns
		self.turnnum = self.turnnum + 1
		print('Current turn: ' + str(self.turnnum) + ' of ' + str(total) + '\n Current work index value: ' + str(self.testvars[index]) + ' (Trail ' + str(index) + ' of ' + str(len(self.testvars)) + ')')
			
	def average(self):
		totalusd = 0
		totalbtc= 0
		totalloss = 0

		for x in range(0, len(self.results.rusd)):
			totalusd = totalusd + self.results.rusd[x]
		avgusd = totalusd / Decimal(len(self.results.rusd))
		self.avgusd = avgusd

		for y in range(0, len(self.results.rusd)):
			totalbtc = totalbtc + self.results.rbtc[y]
		avgbtc = totalbtc / Decimal(len(self.results.rusd))
		self.avgbtc = avgbtc
		
		mlossusd = min(self.results.rusd)
		self.mlossusd = mlossusd
		mgainusd = max(self.results.rusd)
		self.mgainusd = mgainusd
		
		mlossbtc = min(self.results.rbtc)
		self.mlossbtc = mlossbtc
		mgainbtc = max(self.results.rbtc)
		self.mgainbtc = mgainbtc
		
		ind = len(self.results.rusd) - 1
		if self.results.rusd[ind] >= 0:
			self.rungain += 1
		else:
			self.runloss += 1
			self.failloses.append(mlossusd)
		
		if self.runloss != 0 and self.trialturn != 0:
			self.failrate = int(self.runloss / self.trialturn * 100)
		else:
			self.failrate = 0
		
		flosslen = len(self.failloses)
		if flosslen > 0:
			for x in range(0, flosslen):
				totalloss += self.failloses[x]
			avgloss = totalloss / flosslen
			self.avgfailloss = avgloss
				
		return avgusd, avgbtc, mlossusd, mlossbtc
				
	def autotunerun(self, attrib, startval, variance, resume=None):
		resume = self.resume
		escape = False
		saveindex = ('lsavgusd',
		'lsmlossusd',
		'lsavgfailloss',
		'lsrunloss',
		'testvar',
		'avgusdex',
		'mlossusdex',
		'runlossex',
		'testvarex',
		'dcertainty',
		'wincertainty',
		'attrib',
		'self.testattrib',
		'direction',
		'success',
		'newvar',
		'increment',
		'first',
		'certainty',
		'incfactor',
		'cycle',
		'self.turnnum',
		'self.runs',
		'self.trialturn',
		'self.results.rusd',
		'self.results.rbtc',
		'self.rungain',
		'self.runloss',
		'self.avgfailloss',
		'self.failloses',
		'self.failrate',
		'self.timeremain',
		'self.results.turntime',
		'self.stop',
		'self.mlossusd',
		'self.mlossbtc',
		'self.mgainusd',
		'self.mgainbtc',
		'self.avgusd',
		'self.avgbtc',
		'self.newtune',
		'self.tunedattribs',
		'self.tunedvalues',
		'self.bestscore',
		'self.bestval',
		'confidence',
		'posint',
		'ocertainty'
		)
		
		vardic = {'self.results.rusd': self.results.rusd,
		'self.results.rbtc': self.results.rbtc,
		'self.rungain': self.rungain,
		'self.avgfailloss': self.avgfailloss,
		'self.failloses': self.failloses,
		'self.failrate': self.failrate,
		'self.trialturn': self.trialturn,
		'self.timeremain': self.timeremain,
		'self.results.turntime': self.results.turntime,
		'self.runloss': self.runloss,
		'lsavgusd': [],
		'lsmlossusd': [],
		'lsavgfailloss': [],
		'lsrunloss': [],
		'testvar': [],
		'avgusdex': [],
		'mlossusdex': [],
		'runlossex': [],
		'testvarex': [],
		'dcertainty': 0,
		'wincertainty': 0,
		'attrib': attrib,
		'self.testattrib': attrib,
		'direction': False,
		'success': False,
		'newvar': 0,
		'increment': None,
		'first': True,
		'certainty': 0,
		'incfactor': 1,
		'cycle': 0,
		'self.turnnum': 0,
		'self.runs': self.runs,
		'self.trialturn': self.trialturn,
		'self.stop': self.stop,
		'self.mlossusd': self.mlossusd,
		'self.mlossbtc': self.mlossbtc,
		'self.mgainusd': self.mgainusd,
		'self.mgainbtc': self.mgainbtc,
		'self.avgusd': self.avgusd,
		'self.avgbtc': self.avgbtc,
		'self.newtune': self.newtune,
		'self.tunedattribs': self.tunedattribs,
		'self.tunedvalues': self.tunedvalues,
		'self.bestscore': self.bestscore,
		'self.bestval': self.bestval,
		'confidence': 0,
		'posint': False,
		'ocertainty': 0
		}
		
		if resume:
			outinfo = 'RESUME'
			num = ('0','1','2','3','4','5','6','7','8','9')
			ls = ['[', ']']
			flt = ['.']

			with open('finetune.resume', 'r') as resinfo:
				for line in resinfo:
					line = line.strip()
					
					start = 0
					end = line.find('=')
					var = line[start:end]
					
					start = end + 1
					end = line.find(';;')
					val = line[start:end]
					#print('Var: ' + str(var) + ' Val:' + str(val) + 'Type: ' + str(type(val)))
					
					valt = list(val)
					typ = 'str'
					ap = '"'
					for x in range(0, len(valt)):
						if "True" == val or "False" == val:
							typ = 'bool'
							ap = ''
							break
						if valt[x] in ls:
							typ = 'list'
							ap = ''
							break
						if valt[x] in num:
							typ = 'int'
							ap = ''
						if valt[x] in flt:
							typ = 'float'
							ap = ''
							break
					value = eval(typ + '(' + ap + val + ap +')')
					vardic[var] = value
		
		getcontext().prec = 5
		stime = time.time()
		
		comp = 2
		items = ['avgusd', 'avgfailloss', 'runloss', 'mlossusd']
		
		lsavgusd = vardic['lsavgusd']
		lsmlossusd = vardic['lsmlossusd']
		lsavgfailloss = vardic['lsavgfailloss']
		lsrunloss = vardic['lsrunloss']
		testvar = vardic['testvar']
		
		avgusdex = vardic['avgusdex']
		mlossusdex = vardic['mlossusdex']
		runlossex = vardic['runlossex']
		testvarex = vardic['testvarex']
		
		dcertainty = vardic['dcertainty']
		wincertainty = vardic['wincertainty']
		certainty = vardic['certainty']
		
		direction = vardic['direction']
		success = False
		newvar = vardic['newvar']
		first = vardic['first']
		
		attrib = vardic['attrib']
		increment = vardic['increment']
		
		self.runs = vardic['self.runs']
		self.turnnum = vardic['self.turnnum']
		self.trialturn = vardic['self.trialturn']
		self.testattrib = attrib
		if resume:
			self.turnnum -= 1
			self.trialturn -= 1
		
		self.results.rusd = vardic['self.results.rusd']
		self.results.rbtc = vardic['self.results.rbtc']
		self.rungain = vardic['self.rungain']
		self.runloss = vardic['self.runloss']
		self.avgfailloss = vardic['self.avgfailloss']
		self.failloses = vardic['self.failloses']
		self.failrate = vardic['self.failrate']
		self.trialturn = vardic['self.trialturn']
		self.timeremain = vardic['self.timeremain']
		self.results.turntime = vardic['self.results.turntime']
		self.stop = vardic['self.stop']
		
		self.mlossusd = vardic['self.mlossusd']
		self.mlossbtc = vardic['self.mlossbtc']
		self.mgainusd = vardic['self.mgainusd']
		self.mgainbtc = vardic['self.mgainbtc']
		self.avgusd = vardic['self.avgusd']
		self.avgbtc = vardic['self.avgbtc']
		
		self.newtune = vardic['self.newtune']
		self.newtune = vardic['self.tunedattribs']
		self.newtune = vardic['self.tunedvalues']
		self.bestscore = vardic['self.bestscore']
		self.bestval = vardic['self.bestval']
		
		confidence = vardic['confidence']
		posint = vardic['posint']
		ocertainty = vardic['ocertainty']
		
		
		om = 'w+'
				
		
		incfactor = 1
		cycle = 0
		
		if not resume:
			testvar.append(startval)
			increment = startval * variance
			outinfo = 'BEGIN'

		
		with open(self.resultspath + self.testattrib, 'a+') as out:
			out.write('\n\n *** ' + outinfo + ' AUTOTUNE FOR ATTRIBUTE ' + attrib + ' *** \n\n')
							### Resume Point ###
		while True:
			try:
				chngcomp = True
				
				if first:
					if not resume:
						newvar = startval + increment
						testvar.append(newvar)
						
				for x in range(0, len(testvar)):
					if not first:
						x += 1
					if x == len(testvar):
						break
					if not resume:
						self.clresults()
						self.turnnum = 0
					self.testvars = [testvar[x]]
					self.totalruns = self.runs * len(self.testvars)
					print('Self.testvars: ' + str(self.testvars))
					print('Autotune testvars: ' + str(testvar))
					print('Cycle: ' + str(cycle))
					print('X = ' + str(x))
					#input()
					
					avgusd, mloss = self.start(resume)
					if resume:
						resume = False
					
					failloss = self.avgfailloss
					failcnt = self.runloss
					
					for y in range(0, len(items)):
						com = 'ls' + items[y] + '.append(' + str(eval('self.' + items[y])) + ')'
						eval(com)
						
				## prep for score calc, runloss = max loss btc
				#if self.runs >= 50:
				#	rlossadj = 50 / self.runs
				for x in range(0, len(lsmlossusd)):
					lsmlossusd[x] /= 3 ### Reduce effect of maximum run loss, to make other factors more important
				hirunloss = max(lsrunloss)
				hiind = lsrunloss.index(hirunloss)
				if hiind == 0:
					lowind = 1
				else:
					lowind = 0
				lowloss = min(lsrunloss)
				
				penalty = lowloss - hirunloss
				#if self.runs >= 50:
				#	penalty *= rlossadj
				
				scores = []
				for x in range(0, len(testvar)):
					if x == lowind:
						runloss = 0
					else:
						runloss = penalty
					scorecal = self.calcscores(lsavgusd[x], lsmlossusd[x], runloss, lsavgfailloss[x])
					scores.append(scorecal)
				#print('Scores: ' + str(scores) + ' Testvars: ' + str(testvar))
				#input()
				if scores[0] >= scores[1]:
					if scores[0] not in self.bestscore:
						self.bestscore.append(scores[0])
						self.bestval.append(testvar[0])
					direction, increment, newvar, success, dcertainty, wincertainty = self.startvalwin(increment, startval, direction, newvar, wincertainty, incfactor, dcertainty, first, variance)
					if not direction:
						ocertainty += 1 #####################
					target = 0
				else:
					if scores[1] not in self.bestscore:
						if direction:
							if scores[1] <= max(self.bestscore):
								confidence += 1
								if confidence >= 2:
									success = True
						self.bestscore.append(scores[1])
						self.bestval.append(testvar[1])
						
					direction, newvar, dcertainty = self.startvallose(increment, startval, direction, newvar, dcertainty, testvar, first, variance)
					
					target = 1
					
				oldvar = testvar[1]
				#testvar.append(oldvar)
				
				
				### For positive variables, ensure test variable doesnt go below 0 or indecision issues may occur
				if first:
					if testvar[0] > 0:
						posint = True
				if posint:
					if newvar < 0:
						newvar = 0
						increment *= -1
						inc = increment * variance
						newvar += inc
						if incremenet == 0:
							success = True
				if not direction:
					if ocertainty > 2:
						success = True
				if success:
					break
				else:
					for y in range(0, len(items)):
						com = 'ls' + items[y] + '.pop(' + str(0) + ')'
						value = eval(com)
						com2 = items[y] + 'ex.append("' + str(value) + '")'
				testvar[0] = oldvar
				testvar[1] = newvar
				startval = newvar
				first = False
				print('End cycle readout: Oldvar = ' + str(oldvar) + ' Newvar = ' + str(newvar) + ' Testvar = ' + str(testvar) + ' First = ' + str(first))
				cycle += 1
				
				locvars = locals()
				self.savedata(saveindex, locvars, '_auto')
			except KeyboardInterrupt:
				locvars = locals()
				self.savedata(saveindex, locvars, '')
				escape = True
				break
		
		if not escape:
			etime = time.time()
			dur = etime - stime
			durmin = Decimal(dur / 60)
			durhr = durmin / Decimal(60)
			
			best = max(self.bestscore)
			bindex = self.bestscore.index(best)
			bestval = self.bestval[bindex]
			self.bestscore = []
			self.bestval = []
			
			fid = str(randint(0, 9999999999))
			with open(self.resultspath + self.testattrib, 'a+') as out:
				out.write('\nBest variable for attribute "' + attrib + '" determined: ' + str(bestval))
				out.write('\nTotal run time: ' + str(durmin) + ' (min) / ' + str(durhr) + ' (hrs)')
				out.write('\nAI Variables File ID: ' + fid)
				out.write('\n\n *** END AUTOTUNE FOR ATTRIBUTE *** \n\n')
				
			os.system('cp vars.curattrib ' + 'finetune.data/avgresults/' + self.testattrib + '.' + fid)
			self.tunedattribs.append(attrib)
			self.tunedvalues.append(bestval)
			self.tunedtimes.append(durhr)
			
			mde = 'w+'
			with open('tuned.autotune', mde) as tout:
				for i in self.tunedattribs:
					tout.write(i + '\n')
					mde = 'a'
			
			self.newtune = True
		
		return escape
		
	def savedata(self, saveindex, locvars, fname):
		write = 'w+'
		for x in range(0, len(saveindex)):
			savvar = saveindex[x]
			if 'self.' in savvar:
				savval = eval(savvar)
			else:
				savval = eval('locvars["' + saveindex[x] + '"]')
			with open('finetune.resume' + fname, write) as out:
				out.write(str(savvar) + '=' + str(savval) + ';;\n')
			write = 'a+'
	
	def bullshit():
		items = ('runlossex', 'mlossex', 'avgusdex', 'testvarex')
		holders = ('lowfail', 'ind', 'maxloss', 'avgusd', 'var')
		lowfail = []
		ind = []
		maxloss = []
		avgusd = []
		var = []
		
		for y in range(0, 2):
			ind = runlossex.index(testvar[0])
			
			lowfail = runlossex[ind]
			maxloss = mlossex[ind]
			avgusd = avgusdex[ind]
			var = testvar[0]
			for x in range(0, len(items)):
				com = items[x] + '.pop(' + str(ind) + ')'
				val = eval(com)
				com = holders[x] + '.append(' + val + ')'
				
		if lowfail[0] == lowfail[1]:
			zero = maxloss[0] < maxloss[1]
			if not zero:
				target = 1
			if maxloss[0] == maxloss[1]:
				zero = avgusd[0] > avgusd[1]
				if not zero:
					target = 1
			if zero:
				target = 0
		else:
			target = 0
		
	def calcscores(self, avgusd, mloss, runloss, failloss):
		total = 0
		items = ('avgusd', 'mloss', 'runloss', 'failloss') #failloss = average fail loss amount, mloss = maximum btc change mount, avgusd = average usd change, runloss = number of runs it failed to earn usd
		for x in range(0, len(items)):
			val = eval(items[x])
			if items[x] == 'mloss':
				val /= self.runs
			if items[x] == 'avgusd':
				val *= 100 #Add more weight to averages
			#print('Item: ' + str(items[x]) + ' Value: ' + str(val))
			total += val
		#print(total)
		#input()
		return total
					
	def startvalwin(self, increment, startval, direction, newvar, wincertainty, incfactor, dcertainty, first, variance):
		getcontext().prec = 5
		success = False

		increment *= -1
		print('Increment: ' + str(increment))
		if first:
			inc = increment * 2
			newvar += inc
		else:
			increment *= variance * 2
			newvar += increment
		
		print('Direction not yet discovered')
		if direction:
			wincertainty += 1
			if dcertainty >= 1:
				dcertainty -= 1
			direction = False##
			if wincertainty == 2:
				success = True
			
		print('Startval win! '+ str(newvar))

		return direction, increment, newvar, success, dcertainty, wincertainty
		
	def startvallose(self, increment, startval, direction, newvar, dcertainty, testvar, first, variance):
		getcontext().prec = 5
		startval = testvar[1]
		if not direction:
			if first:
				newvar = startval + increment
				print('Direction not yet discovered')
			else:
				increment *= variance
				newvar += increment
		else:
			increment *= variance
			newvar += increment
		dcertainty += 1
		if dcertainty > 1:
			direction = True
		else:
			direction = False
		print('Startval lose! '+ str(newvar))

		return direction, newvar, dcertainty
				

	def start(self, resume=False):
			end = False
			data0 = ''
			for z in range(0, len(self.testvars)):
				if not end:
					try:
						index = z
						if z == self.stop:
							break
						testvar = self.testvars[z]
						trials = self.runs
						if resume:
							trials = self.runs - self.turnnum
						for x in range(0, trials):
								self.trialturn += 1
								self.totalturns(index)
								self.runsim(testvar, index)
								avgusd, avgbtc, mlossusd, mlossbtc = self.average()
					except KeyboardInterrupt:
						if self.auto:
							raise KeyboardInterrupt
						end = True
						
						data0 = '**KEYBOARD INTERRUPT**'
						
					
					if self.auto:
						data0 += '!!!AUTOTUNE!!!'
					data1 = data0 + '\nTesting: ' + self.testattrib + '\n' + '>> Attribute value: ' + str(testvar) + '\n'
					data2 = str(self.runs) + ' turn average: \n' + str(avgusd) + ' (USD)\n' + str(avgbtc) + ' (BTC) \n' + ' Max loss USD: ' + str(mlossusd) + ' Max loss BTC: ' + str(mlossbtc)
					data3 = '\nGain Count: ' + str(self.rungain) + ' Loss Count: ' + str(self.runloss) + ' Fail Rate: ' + str(self.failrate) + '\nAccuracy: +/-' + str(self.accuracy) + '% Avg. Fail loss: ' + str(self.avgfailloss) + ' \n\n'

					with open(self.resultspath + self.testattrib, 'a+') as out:
						out.write(data1)
						out.write(data2)
						out.write(data3)
						
					
					if self.auto:
						
						return avgbtc, self.mlossbtc
						
					self.clresults()
				
	def loaddata(self):
		try:
			fdir = 'saved_data/'
			for x in range(0, len(self.saveitems)):
				with open(fdir + self.saveitems[x], 'r') as load:
					for line in load:
						line = line.strip()
						com = 'self.' + self.saveditems[x] + '.append("' + line + '")'
						eval(com)
		except FileNotFoundError:
			print('Error loading saved files!')
			input('Press enter to continue')
					
	def clresults(self):
		self.results.rusd = []
		self.results.rbtc = []
		self.rungain = 0
		self.runloss = 0
		self.avgfailloss = 0
		self.failloses = []
		self.failrate = 0
		self.trialturn = 0
		self.timeremain = ['Not established']
		self.results.turntime = []

com = "Finetune('" + curver + "')"
exec(com)
