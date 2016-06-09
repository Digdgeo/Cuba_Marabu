import os, shutil, re, time, subprocess, pandas, rasterio, pymongo, sys, fileinput, stat, urllib
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy import ndimage
from osgeo import gdal, gdalconst, ogr
from pymasker import landsatmasker, confidence
from datetime import datetime


class nor(object):

    '''esta clase realiza la normalizacion entre distintas fechas de la misma escena, de cara a obtener un buen producto en la aplicacion
    del proximo metodo aplicada BQA, en el que se reemplazaran los pixeles nubosos de la escena de referencia por pixeles de otras escenas'''

    def __init__(self, ruta_rad):


        self.ruta_rad = ruta_rad
        self.escena = os.path.split(self.ruta_rad)[1]
        self.rad = os.path.split(self.ruta_rad)[0]
        self.raiz = os.path.split(self.rad)[0]
        self.nor = os.path.join(self.raiz, 'nor')
        self.pias = r'C:\Cuba\data\Pias_014_045.tif'
        self.parametrosnor = {}
        self.iter = 1


    def normalize(self):
        
        '''-----\n
        Este metodo controlo el flujo de la normalizacion, si no se llegan a obtener los coeficientes (R>0.85 y N_Pixeles >= 10,
        va pasando hacia el siguiente nivel, hasta que se logran obtener esos valores o hasta que se llega al ultimo paso)'''
        
                        
        lstbandas = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7']
         
        
        for i in os.listdir(self.ruta_rad):
            
            banda = os.path.join(self.ruta_rad, i)

            banda_num = banda[-6:-4]

            if banda_num in lstbandas and i.endswith('.img'):
                
                print banda, ' desde normalize'

                self.nor1(banda, self.pias)
                #Probar a hacerlo con una lista de funciones
                if banda_num not in self.parametrosnor.keys():
                    self.iter = 1
                    self.iter += 1
                    self.nor1(banda, self.pias, std = 22)
                    if banda_num not in self.parametrosnor.keys():
                        self.iter += 1
                        self.nor1(banda, self.pias, std = 33)
                        if banda_num not in self.parametrosnor.keys():
                            self.iter += 1     
                        else:
                            print 'No se ha podido normalizar la banda ', banda_num
                                    
            #Una vez acabados los bucles guardamos los coeficientes en un txt. Redundante pero asi hay 
            #que hacerlo porque quiere David
            path_nor = os.path.join(self.nor, self.escena)
            if not os.path.exists(path_nor):
                os.makedirs(path_nor)
            arc = os.path.join(path_nor, 'coeficientes.txt')
            f = open(arc, 'w')
            for i in sorted(self.parametrosnor.items()):
                f.write(str(i)+'\n')
            f.close()  
            
            

    def nor1(self, banda, mascara, std = 11):
        
        '''-----\n
        Este metodo busca obtiene los coeficientes necesarios para llevar a cabo la normalizacion,
        tanto en nor1 como en nor1bis'''

        print 'comenzando nor1'
        print banda, mascara, std

        #Ruta a las bandas usadas para normalizar
        ref = os.path.join(self.rad, '20151216l8oli014_045')
        path_b1 = os.path.join(ref, '20151216l8oli014_045_r_b1.img')
        path_b2 = os.path.join(ref, '20151216l8oli014_045_r_b2.img')
        path_b3 = os.path.join(ref, '20151216l8oli014_045_r_b3.img')
        path_b4 = os.path.join(ref, '20151216l8oli014_045_r_b4.img')
        path_b5 = os.path.join(ref, '20151216l8oli014_045_r_b5.img')
        path_b6 = os.path.join(ref, '20151216l8oli014_045_r_b6.img')
        path_b7 = os.path.join(ref, '20151216l8oli014_045_r_b7.img')

        dnorbandas = {'b1': path_b1, 'b2': path_b2, 'b3': path_b3, 'b4': path_b4, 'b5': path_b5, 'b6': path_b6, 'b7': path_b7}
        
        
        for i in os.listdir(self.ruta_rad):

            if i.endswith('Fmask.img'):
                mask_nubes = os.path.join(self.ruta_rad, i)
                print 'Mascara de nubes: ', mask_nubes

        pia_mask = r'C:\Cuba\data\Pias_014_045.tif' #HAY 4020 PIXELES

        print 'mascara pias: ', mascara

        with rasterio.open(pia_mask) as src:
            mask1 = src.read()
        with rasterio.open(mask_nubes) as src:
            cloud = src.read()
            #pasamos la mascara a binaria 0 despejado, 1 nubes y sombra de nubes
            cloud[(cloud!=2)|(cloud!=4)] = 0
            cloud[(cloud==2)|(cloud==4)] = 1

        banda_num = banda[-6:-4]
        print banda_num
        
        if banda_num in dnorbandas.keys():
            with rasterio.open(banda) as src:
                current = src.read()
            #Aqui con el diccionario nos aseguramos de que estamos comparando cada banda con su homologa del 20020718
            with rasterio.open(dnorbandas[banda_num]) as src:
                ref = src.read()
            #Ya tenemos todas las bandas de la imagen actual y de la imagen de referencia leidas como array

            #Aplicamos la mascara de las PIAs
            mask_curr_pia = np.ma.masked_where(mask1!=1,current)
            mask_ref_pia = np.ma.masked_where(mask1!=1,ref)
            cloud_pias = np.ma.masked_where(mask1!=1,cloud)
            #hemos aplicado la mascara y ahora guardamos una nueva matriz con la mascara aplicamos
            ref_PIA = np.ma.compressed(mask_ref_pia)
            current_PIA = np.ma.compressed(mask_curr_pia)
            cloud_PIA = np.ma.compressed(cloud_pias)

            #Aplicamos la mascara de NoData HABRIA QUE PONER EL NODATA DE FLOAT 32!!!!!!!!!!!!!
            #LO VOY A QUITAR DE MOMENTO 310516
            

            #Aplicamos la mascara de Nubes. se toma 1 porque se han igualado las 2 mascaras (Fmask y BQA)
            cloud_current_mask = np.ma.masked_where((cloud_PIA==1),current_PIA)
            cloud_ref_mask = np.ma.masked_where((cloud_PIA==1),ref_PIA)
            #cloud_pias_mask = np.ma.masked_where((cloud_PIA==1),pias_PIA_NoData)

            ref_PIA_Cloud_NoData = np.ma.compressed(cloud_ref_mask)
            current_PIA_Cloud_NoData = np.ma.compressed(cloud_current_mask)
            #pias_PIA_Cloud_NoData = np.ma.compressed(cloud_pias_mask)


            #Realizamos la 1 regresion
            slope, intercept, r_value, p_value, std_err = linregress(current_PIA_Cloud_NoData,ref_PIA_Cloud_NoData)
            print '1 regresion: slope: '+ str(slope), 'intercept:', intercept, 'r', r_value, 'N:', len(ref_PIA_Cloud_NoData)
            print '++++++++++++++++++++++++++++++++\n'

            #Ahora tenemos los parametros para obtener el residuo de la primera regresion y 
            #eliminar aquellos que son mayores de abs(11.113949)
            esperado = current_PIA_Cloud_NoData * slope + intercept
            residuo = ref_PIA_Cloud_NoData - esperado

            mask_current_PIA_NoData_STD = np.ma.masked_where(abs(residuo)>=int(std), current_PIA_Cloud_NoData)
            mask_ref_PIA_NoData_STD = np.ma.masked_where(abs(residuo)>=int(std),ref_PIA_Cloud_NoData)
            #mask_pias_PIA_NoData_STD = np.ma.masked_where(abs(residuo)>=int(std),pias_PIA_Cloud_NoData)
            current_PIA_NoData_STD = np.ma.compressed(mask_current_PIA_NoData_STD)
            ref_PIA_NoData_STD = np.ma.compressed(mask_ref_PIA_NoData_STD)
            #pias_PIA_NoData_STD = np.ma.compressed(mask_pias_PIA_NoData_STD)

            #Hemos enmascarado los resiudos, ahora calculamos la 2 regresion
            slope, intercept, r_value, p_value, std_err = linregress(current_PIA_NoData_STD,ref_PIA_NoData_STD)
            print '\n++++++++++++++++++++++++++++++++++'
            print 'slope: '+ str(slope), 'intercept:', intercept, 'r', r_value, 'N:', len(ref_PIA_NoData_STD)
            print '++++++++++++++++++++++++++++++++++\n'
            
            #si r squared es mayor q 0.85 y al menos se han usado la mitad de los pixeles de las pias
            if r_value > 0.75 and len(ref_PIA_NoData_STD) > 2010: 

                self.parametrosnor[banda_num]= {'Parametros':{'slope': slope, 'intercept': intercept, 'r': r_value, 'N': len(ref_PIA_NoData_STD), 'iter': self.iter}}
                
                print 'parametros en nor1: ', self.parametrosnor
                print '\comenzando nor2\n'
                self.nor2l8(banda, slope, intercept)#llamamos a nor2, Tambien funciona con L7
                print '\nNormalizacion de ', banda_num, ' realizada.\n'
            else:
                pass


    def nor2l8(self, banda, slope, intercept):
    
        '''-----\n
        Este metodo aplica la ecuacion de la recta de regresion a cada banda (siempre que los haya podido obtener)'''
        
        #path_geo = os.path.join(self.geo, self.escena)
        path_nor_escena = os.path.join(self.nor, self.escena)
        if not os.path.exists(path_nor_escena):
            os.makedirs(path_nor_escena)
        banda_num = banda[-6:-4]
        outFile = os.path.join(path_nor_escena, self.escena + '_grn1_' + banda_num + '.img')
        
        #Abrimos la banda y le aplicamos la ecuacion
        with rasterio.open(banda) as src:

            rs = src.read()
            rs = rs*slope+intercept

            min_msk =  (rs < 0)             
            max_msk = (rs>=1)

            rs[min_msk] = 0
            rs[max_msk] = 1

            profile = src.meta
            profile.update(dtype=rasterio.float32)

            with rasterio.open(outFile, 'w', **profile) as dst:
                dst.write(rs.astype(rasterio.float32))
       