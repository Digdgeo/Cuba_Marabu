######## PROTOCOLO AUTOMATICO PARA LA CORRECCION RADIOMETRICA DE ESCENAS LANDSAT 8 #######
######                                                                              ######
####                        Autor: Diego Garcia Diaz                                  ####
###                      email: digd.geografo@gmail.com                                ###
##                 GitHub: https://github.com/Digdgeo/Cuba_Marabu                       ##
#                   Universidad de Huelva 25/05/2016-25/07/2016                          #

# coding: utf-8

import os, rasterio, re

class bpa():


	'''Esta clase tiene por fin implemetar el  metodo de mejor pixel disponible en una serie de escenas Landsat 8. En principio 
	esta pensada para ser aplicada dentro del proyecto de la UHU "xxxxx" debido a la cantidad de nubes que encontramos en 
	todas las escenas de Cuba. La idea es coger una serie de fechas por cada escena (fundanentalmente entre 3 y 5) lo mas proximas 
	entre si temporalmente y hacer filtros en base a la presencia o no de nubes. De modo que los pixeles con nubes (o sombra de nubes) 
	seran sustituidos por los pixeles sin nubes de la escena mas proxima. La mascara de nubes empleada es Fmask (*')'''

	def __init__(self, ruta_rad, path, row):

		#Iniciamos la clase. La ruta debe ser a una escena Landsat 8 corregida radiomericamente
		self.ruta_rad = ruta_rad
		self.path = path
		self.row = row
		self.raiz = os.path.split(self.ruta_rad)[0]
		self.ori = os.path.join(self.raiz, 'ori')
		#esto es una lista que nos guardara todas las escenas de nuestro path y row
		self.lpr = []
		self.lpr_fm = {}
		self.b1 = []

		for i in os.listdir(self.ruta_rad):


			self.escena = i
			self.ruta_escena = os.path.join(self.ruta_rad, self.escena)
			if os.path.isdir(self.ruta_escena):

				#print self.escena[-6:-4], self.escena[-2:]

				if int(self.escena[-6:-4]) == self.path and int(self.escena[-2:]) == self.row:
					
					self.lpr.append(self.ruta_escena)

		print self.lpr


	def get_fm(self):

		'''este metodo crea un diccionario con las fechas de la escena en cuestion y sus mascaras de nubes'''

		for i in self.lpr:

			self.ruta_ori = os.path.join(self.ori, os.path.split(i)[1])
			for f in os.listdir(self.ruta_ori):
				if f.endswith('Fmask.img'):
					Fmask = os.path.join(self.ruta_ori, f)
					self.lpr_fm[i] = Fmask

		for i, ii in sorted(self.lpr_fm.items(), reverse = True):
			print i, ii

	
	def process(self):

		'''este metodo realizara el proceso de combinar entre si los pixeles de las distintas fechas de la escena, filtrando los
		pixeles con nubes y sombras de nubes'''

		
		#for esc, fm in self.lpr_fm.items():
		

		keys = [os.path.split(i)[1][:-4]  for i in self.lpr_fm.keys()]
		clouds = [i + '_fm' for i in keys]
		count = 0
		

		for esc, fm in self.lpr_fm.items():

			for i in os.listdir(esc):

				if i.endswith('b1.img'):

					b1 = os.path.join(esc, i)
					self.b1.append(b1)

				'''with rasterio.open(esc) as src:
					keys[count] = src.read()
				with rasterio.open(fm) as src:
					clouds[count] = src.read()'''

		print self.b1

	