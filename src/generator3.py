#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from file_manager import FileManager

class Generator(FileManager):
	
	extension = ['@gmail.com','@hotmail.com','@yahoo.com','@company.com']
	extras = ['_','1','2','3','4','5','6','7','8','9']
	consonantes = ['B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z']
	vocales = ['A','E','I','O','U']

	def before_buil(self,data):
		iterar = []
		array = data.split(',')
		
		for row in array:
			if row.count('"') > 0:
				row = row.replace('"','')
				r = self.build_string(row)
				r = str(r)
				if r.isdigit() == False:
					if r.count(',') > 0:
						r = r.replace(',','","')
				r = '"'+r+'"'
				iterar.append(r)
			else:
				r = self.build_string(row)
				iterar.append(r)
		return iterar

	def build_string(self,data):
		if data.count(':') > 0:
			data = data.replace('[','')
			data = data.replace(']','')
			array = data.split(':')
			data = random.randint(int(array[0]),int(array[1]))
		elif data.count('E-mail') > 0:
			data = self.generar_email()
		elif data.count('Password') > 0:
			data = self.generar_password(8)
		elif data.count('_()') > 0:
			data = data.replace('_()','')
			data = data.lower() + '.txt'
			array1 = self.return_data_file_array(data)
			dato = random.choice(array1)
			array2 = dato.split(' ')
			data = array2[0]+','+array2[1]
		elif data.count('-') > 1:
			data = data.replace('[','')
			data = data.replace(']','')
			array = data.split('-')
			data = random.choice(array)
		elif data.count('DATE(') > 0:
			data = data.replace(')','')
			data = data.replace('DATE(','')
		else:
			#print(data)
			data = data.lower() + '.txt'
			r = self.return_data_file_array(data)
			#print(r)
			if r =='Error':
				data = data.replace('.txt','')
				#print(data)
				if data.count(' ') > 0:
					dato = ''
					for x in data.split(' '):
						x = x+'.txt'
						m = self.return_data_file_array(x)
						if m.count('Error') > 0:
							x = x.replace('.txt','')
							dato = dato + str(x) + ' '
						else:
							dato = dato + str(random.choice(m)) + ' '
					data = dato.rstrip(' ')
			else:
				data = random.choice(r)
				if data.count(' ') > 0:
					array = data.split(' ')
					data = array[0]
		return data

	def generar_email(self):
		mail = ''
		for x in xrange(1,4):
			mail = mail + random.choice(self.vocales) + random.choice(self.consonantes)
		
		for x in xrange(0,2):
			mail = mail + random.choice(self.extras) + random.choice(self.extras)

		mail = mail + random.choice(self.extension)

		return mail

	def generar_password(self,password_extension):
		n = int(password_extension) / 2
		password = ''

		for x in xrange(0,n):
			password = password + random.choice(self.consonantes) + random.choice(self.vocales)
		
		return password

	def fecha(self,orden):
		data = orden.count()
		almacen = ''

	def lista_archivos(self):
		r = self.file_lists()
		lista = []
		for row in r.split('\n'):
			row = row.replace('.txt','')
			lista.append(row.capitalize())
		lista.pop()
		return lista

	def crear_sql(self,tabla,data):
		sql = 'INSERT INTO '+ tabla + '('
		columns = ''
		for row in data:
			columns = columns + row + ','
		columns = columns.rstrip(',')
		sql = sql + columns + ') VALUES('
		return sql

	def preparar_consulta(self,pos_sql,data):
		sql = pos_sql
		query = ''
		for row in data:
			query = query + str(row) + ','
		query = query.rstrip(',')
		sql = sql + query + ');'
		return sql