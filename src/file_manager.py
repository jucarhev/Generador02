#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from subprocess import PIPE, Popen
import os
import random

class FileManager():
	""" Class FileManager """

	def file_open(self,file,ruta=''):
		try:
			if ruta == '':
				ruta = 'diccionary/'
			f = open(ruta+file, "rw")
			archivo = f.read()
			f.close()
			return archivo
		except Exception as e:
			return e
		
	def write_file(self,file,content,ruta="diccionary/"):
		try:
			f = open(ruta+file, "w")
			archivo = f.write(content)
			f.close()
		except Exception as e:
			return 'Error'
		
	def return_data_file_array(self,file,ruta=''):
		try:
			if ruta == '':
				ruta = 'diccionary/'
			contenido = self.file_open(file,ruta)
			array = contenido.split('\n')
			return array
		except Exception as e:
			return 'Error'

	def update_content_file(self,file,content,ruta=''):
		try:
			if ruta == '':
				ruta = 'diccionary/'
			contenido = self.file_open(file,ruta)
			if contenido != 'Error':
				contenido = ''
				content = content.replace(',','\n')
				contenido = content + contenido
				self.write_file(file,contenido,ruta)
				return True
			else:
				return 'Error'
		except Exception as e:
			return 'Error'

	def file_lists(self):
		ruta = os.getcwd()
		nueva_ruta = os.chdir(ruta + '/diccionary')
		
		proceso = Popen(['ls'], stdout=PIPE, stderr=PIPE)
		error_encontrado = proceso.stderr.read()
		proceso.stderr.close()
		listado = proceso.stdout.read()
		proceso.stdout.close()
		ruta = os.chdir(ruta)

		if not error_encontrado:
			return listado
		else:
			return 'Error'

	def delete_file(self,file):
		try:
			os.remove(os.getcwd() + '/diccionary/' + archivo + '.txt')
		except Exception as e:
			return 'Error'

	def new_file(self,file,content):
		try:
			f = open("diccionary/"+file, "w")
			archivo = f.write(content)
			f.close()
		except Exception as e:
			return 'Error'

#archivo = FileManager()
#print(archivo.file_lists())