import sqlite3
import datetime
import time
import os

class Sqai(object):
	
	def __init__(self, name, **kwargs):
		
		self.name = name
		kwargs['name'] = name
		
		self.connectdb()
		
	def connectdb(self):
		self.conn = sqlite3.connect('cryptai.db')
		self.c = self.conn.cursor()
		
	def getdat(self, returndata, currency, dataitem, sterm, mode):
		if mode != 'count':
			com = 'SELECT ' + returndata + ' FROM ' + currency + ' WHERE ' + dataitem + '=?'
			self.c.execute(com, (sterm,))
			if mode == 'one':
				result = self.c.fetchone()
			if mode == 'all' or mode == 'alldata':
				result = self.c.fetchall()
		else:
			com = 'SELECT ' + returndata + ' FROM ' + currency
			self.c.execute(com)
			result = self.c.fetchone()
		return result
		
	def closedb(self):
		self.conn.close()

