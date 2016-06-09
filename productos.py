######## PROTOCOLO AUTOMATICO PARA LA CORRECCION RADIOMETRICA DE ESCENAS LANDSAT 8 #######
######                                                                              ######
####                        Autor: Diego Garcia Diaz                                  ####
###                      email: digd.geografo@gmail.com                                ###
##                 GitHub: https://github.com/Digdgeo/Cuba_Marabu                       ##
#                   Universidad de Huelva 25/05/2016-25/07/2016                          #

# coding: utf-8

import os, shutil, re, time, subprocess, pandas, rasterio, sys, urllib, fiona, sqlite3, math
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal, gdalconst
from datetime import datetime, date

class Product(object):
    
    def __init__(self, ruta_cdr):
        
        
        self.ruta_escena = ruta_cdr
        self.escena = os.path.split(self.ruta_escena)[1]
        self.raiz = os.path.split(os.path.split(self.ruta_escena)[0])[0]
        print self.raiz
        self.rad = os.path.join(self.raiz, os.path.join('rad', self.escena))
        print self.rad
        self.ori = os.path.join(self.raiz, os.path.join('ori', self.escena))
        self.data = os.path.join(self.raiz, 'data')
        self.temp = os.path.join(self.data, 'temp')
        self.productos = os.path.join(self.raiz, 'productos')
        self.vals = {}
        self.d = {}
        self.pro_esc = os.path.join(self.productos, self.escena)
        if not os.path.exists(self.pro_esc):
            os.makedirs(self.pro_esc)
        if 'l8oli' in self.ruta_escena:
            self.sat = 'L8'
        elif 'se2A' in self.ruta_escena:
            self.sat =  'S2A'
        else:
            print 'No identifico el satelite'

        if self.sat == 'L8':

            for i in os.listdir(self.rad):
                if re.search('img$', i):
                    
                    banda = i[-5]
                                        
                    if banda == '1':
                        self.b1 = os.path.join(self.rad, i)
                    elif banda == '2':
                        self.b2 = os.path.join(self.rad, i)
                    elif banda == '3':
                        self.b3 = os.path.join(self.rad, i)
                    elif banda == '4':
                        self.b4 = os.path.join(self.rad, i)
                    elif banda == '5':
                        self.b5 = os.path.join(self.rad, i)
                    elif banda == '6':
                        self.b6 = os.path.join(self.rad, i)
                    elif banda == '7':
                        self.b7 = os.path.join(self.rad, i)
                    
        
        elif self.sat == 'S2A':


            for i in os.listdir(self.rad):
                if re.search('tif$', i):
                    
                    banda = i[-7:-4]
                   
                    if banda == 'B01':
                        self.b1 = os.path.join(self.rad, i)
                    elif banda == 'B02':
                        self.b2 = os.path.join(self.rad, i)
                    elif banda == 'B03':
                        self.b3 = os.path.join(self.rad, i)
                    elif banda == 'B04':
                        self.b4 = os.path.join(self.rad, i)
                    elif banda == 'B05':
                        self.b5 = os.path.join(self.rad, i)
                    elif banda == 'B06':
                        self.b6 = os.path.join(self.rad, i)
                    elif banda == 'B07':
                        self.b7 = os.path.join(self.rad, i)
                    elif banda == 'B08':
                        self.b8 = os.path.join(self.rad, i)
                    elif banda == 'B8A':
                        self.b8a = os.path.join(self.rad, i)
                    elif banda == 'B09':
                        self.b9 = os.path.join(self.rad, i)
                    elif banda == 'B10':
                        self.b10 = os.path.join(self.rad, i)
                    elif banda == 'B11':
                        self.b11 = os.path.join(self.rad, i)
                    elif banda == 'B12':
                        self.b12 = os.path.join(self.rad, i)

    
        
    def ndvi(self):

        outfile = os.path.join(self.productos, self.escena + '_ndvi.img')
        print outfile
        
        if self.sat == 'L8':
            
            with rasterio.open(self.b5) as nir:
                NIR = nir.read()
                
            with rasterio.open(self.b4) as red:
                RED = red.read()
            
            num = NIR-RED
            den = NIR+RED
            ndvi = num/den
            
            profile = nir.meta
            profile.update(dtype=rasterio.float32)

            with rasterio.open(outfile, 'w', **profile) as dst:
                dst.write(ndvi.astype(rasterio.float32))
    


    def ndwi(self):

        outfile = os.path.join(self.productos, self.escena + '_ndwi.img')
        print outfile
        
        if self.sat == 'L8':
            
            with rasterio.open(self.b5) as nir:
                NIR = nir.read()
                
            with rasterio.open(self.b3) as green:
                GREEN = green.read()
            
            num = GREEN-NIR
            den = GREEN+NIR
            ndwi = num/den
            
            profile = nir.meta
            profile.update(dtype=rasterio.float32)

            with rasterio.open(outfile, 'w', **profile) as dst:
                dst.write(ndwi.astype(rasterio.float32))


    def mndwi(self):

        outfile = os.path.join(self.productos, self.escena + '_mndwi.img')
        print outfile
        
        if self.sat == 'L8':
            
            with rasterio.open(self.b6) as swir1:
                SWIR1 = swir1.read()
                
            with rasterio.open(self.b3) as green:
                GREEN = green.read()
            
            num = GREEN-SWIR1
            den = GREEN+SWIR1
            mndwi = num/den
            
            profile = swir1.meta
            profile.update(dtype=rasterio.float32)

            with rasterio.open(outfile, 'w', **profile) as dst:
                dst.write(mndwi.astype(rasterio.float32)) 


    def evi(self):

        outfile = os.path.join(self.productos, self.escena + '_evi.img')
        print outfile
        
        if self.sat == 'L8':
            
            with rasterio.open(self.b5) as nir:
                NIR = nir.read()
                
            with rasterio.open(self.b4) as red:
                RED = red.read()

            with rasterio.open(self.b2) as blue:
                BLUE = blue.read()
            
            evi = np.true_divide((NIR-RED), (NIR + (6 * RED) - ((7.5 * BLUE) + 1))
            
            profile = nir.meta
            profile.update(dtype=rasterio.float32)

            with rasterio.open(outfile, 'w', **profile) as dst:
                dst.write(nir.astype(rasterio.float32))



    def savi(self):

        outfile = os.path.join(self.productos, self.escena + '_savi.img')
        print outfile
        
        if self.sat == 'L8':
            
            with rasterio.open(self.b5) as nir:
                NIR = nir.read()
                
            with rasterio.open(self.b4) as red:
                RED = red.read()
            
            savi = np.true_divide((NIR-RED), ((NIR + RED + 0.5) * 1.5)
            
            profile = nir.meta
            profile.update(dtype=rasterio.float32)

            with rasterio.open(outfile, 'w', **profile) as dst:
                dst.write(savi.astype(rasterio.float32))


    def msavi(self):

        outfile = os.path.join(self.productos, self.escena + '_msavi.img')
        print outfile
        
        if self.sat == 'L8':
            
            with rasterio.open(self.b5) as nir:
                NIR = nir.read()
                
            with rasterio.open(self.b4) as red:
                RED = red.read()
            
            savi = np.true_divide(2 * NIR + 1 - (np.sqrt(np.power((2 * NIR + 1), 2) - 8 * (NIR - RED), 2)))
            
            profile = nir.meta
            profile.update(dtype=rasterio.float32)

            with rasterio.open(outfile, 'w', **profile) as dst:
                dst.write(savi.astype(rasterio.float32)) 


class Temperatura(Product):


    def toab10(self):

        '''En este metodo calculamos la reflectancia en el techo de la atmosfera de la banda 10 de Landsat 8'''

        indice = 'lst'
        desc = 'Temperatura en superficie corregida con la emisividad de la superficie'
        #enlace = http://www.hindawi.com/journals/js/2016/1480307/

        #outtermal = os.path.join(self.pro_esc, self.escena + '_brigthThermal.img')
        #outndvi = os.path.join(self.pro_esc, self.escena + '_ndvi.img')
        #outpv = os.path.join(self.pro_esc, self.escena + '_pv.img')
        #outemi = os.path.join(self.pro_esc, self.escena + '_emisividad.img')
        outlst = os.path.join(self.pro_esc, self.escena + '_lst.img')
        if os.path.exists(outlst):
            os.remove(outlst)

        if self.sat == 'L8':

            for i in os.listdir(self.ruta_escena):

                #Abrimos el MTL para tomar los valores de las constantes
                if i.endswith('MTL.txt'):
                    mtl = os.path.join(self.ruta_escena,i)
                    arc = open(mtl,'r')
                    for i in arc:
                        if 'K1_CONSTANT_BAND_10' in i:
                            k1_b10 = float(i.split('=')[1])
                        elif 'K2_CONSTANT_BAND_10' in i:
                            k2_b10 = float(i.split('=')[1])
                        elif 'RADIANCE_MULT_BAND_10' in i:
                            mult_b10 = float(i.split('=')[1])
                            print mult_b10
                        elif 'RADIANCE_ADD_BAND_10' in i:
                            add_b10 = float(i.split('=')[1])
                            print add_b10


                            
                elif re.search('B10.TIF$', i):
                    
                    b10 = os.path.join(self.ruta_escena, i)

            #Calculamos la Reflectancia en el techo de la atmosfera para la banda 10
            with rasterio.open(b10) as ter1:
                TER1 = ter1.read()

            toa_b10 = ((mult_b10 * TER1) + add_b10) -0.29

            #Ahora vamos a calcular la temperatura en el techo de la atmosfera (temperatura de brillo) en Celsius
            BT = (np.true_divide(k2_b10, (np.log(np.true_divide(k1_b10, toa_b10)+1)))-273.15)

            
            profile = ter1.meta
            profile.update(dtype=rasterio.float32)

            #with rasterio.open(outfile, 'w', **profile) as dst:
                #dst.write(BT.astype(rasterio.float32)) 

            #Ahora vamos a calcular la emisividad de la superficie, para ello primero debemos de calcular el NDVI
            #Vamos a calcularlo de la escena normalizada
            for i in os.listdir(self.rad):
                if i.endswith('b4.img'):
                    b4 = os.path.join(self.rad, i)
                    print b4
                elif i.endswith('b5.img'):
                    b5 = os.path.join(self.rad, i)
                    print b5

            with rasterio.open(b4) as red:
                RED = red.read()
                
            with rasterio.open(b5) as nir:
                NIR = nir.read()
            
            ndvi = np.true_divide((NIR-RED), (NIR+RED))
            

            #with rasterio.open(outndvi, 'w', **profile) as dst:
                #dst.write(ndvi.astype(rasterio.float32)) 

            #Ahora calculamos la proporcion de vegetacion para calcular la emisividad de la superficie
            #Como solo nos interesa el agua seria mejor dejar un valor fijo de 0.991!!!!!!!!!!!!!!!!!!!!!!!!!!
            pv = np.power(np.true_divide(ndvi-np.nanmin(ndvi), np.nanmax(ndvi)-ndvi), 2)
            e = 0.004 * pv + 0.986

            #with rasterio.open(outpv, 'w', **profile) as dst:
                #dst.write(pv.astype(rasterio.float32)) 

            #with rasterio.open(outemi, 'w', **profile) as dst:
                #dst.write(e.astype(rasterio.float32)) 

            #Ahora calculamos la tempreatura de superficie 
            #lst = np.true_divide(BT, (1 + (np.true_divide((10.895 * BT), 0.014394744927536233) * np.log(e)))
            den = 1 + (10.895 * (np.true_divide(BT,14380)) * np.log(0.991)) 
            lst = np.true_divide(BT, den)

            with rasterio.open(outlst, 'w', **profile) as dst:
                dst.write(lst.astype(rasterio.float32)) 

        else: 

            print 'Solo puedo calcular la temperatura con Landsat 8'

        self.get_val_indice(outlst, indice, desc)
        self.recorte(self.ori, outlst)