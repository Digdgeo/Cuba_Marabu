
import os, rasterio, fiona, gdal, subprocess

#Declaramos las variables con los rasters
l82014 = r'E:\CUBAFINAL\L2014\l82014_22o\Marabul2014.tif'
l82016 = r'E:\CUBAFINAL\L2016\l82016\class_l82016.tif'
s2a = r'E:\CUBAFINAL\S2\s2a_fin\s2a_fin_rsmp.tif'
L2014CM = r'E:\CUBAFINAL\nubes\clouds_l82014.tif'
L2016B1 = r'E:\CUBAFINAL\nubes\clouds_l82016.tif'
s2aCM = r'E:\CUBAFINAL\nubes\clouds_s2a.tif'
slope = r'E:\CUBAFINAL\slope\cubaslope.tif'
rstlist = [l82014, l82016, s2a, L2014CM, L2016B1, s2aCM, slope]
#Declaramos las variables con el shp path y la lista de las cuadriculas
shp_path = r'E:\CUBAFINAL\Rejilla\split\cubasplit'
shplist = [os.path.join(shp_path, i) for i in os.listdir(shp_path) if i.endswith('.shp')]

crop = "-crop_to_cutline"

d = {}
#Empezamos a hacer el loop por la lista de shp recortando cada raster con la extension de la cuadricula
for s in shplist:
    
    d[s] = []
    
    for r in rstlist:
        
        #usamos Gdalwarp para realizar las mascaras, llamandolo desde el modulo subprocess
        cmd = ["gdalwarp", "-dstnodata" , "0" , "-tr",  "30", "30", "-tap", "-cutline"]
        path_masks = os.path.join(r'E:\CUBAFINAL', 'mask_')
        if not os.path.exists(path_masks):
            os.makedirs(path_masks)

        nombre = os.path.join(path_masks, os.path.split(s)[1][:-4] + '_' + os.path.split(r)[1])
        print(nombre)
        salida = os.path.join(path_masks, nombre)
        cmd.append(s)
        cmd.append(crop)
        cmd.append(r)
        cmd.append(salida)

        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr=proc.communicate()
        exit_code=proc.wait()

        if exit_code: 
            raise RuntimeError(stderr)  
        d[s].append(salida)
        
    #Ahora anadimos el area de tierra en ese tile
    for i in os.listdir(r'E:\CUBAFINAL\Rejilla\split\cubasplit'):

        if os.path.split(s)[1] in i and i.endswith('.shp'):

            print('tile', s, 'rec', i, 'area')
            cubashp = fiona.open(os.path.join(r'E:\CUBAFINAL\Rejilla\split\cubasplit', i))
            #d[s].append(cubashp['properties']['area'])
            for p in cubashp:
                #print(p['properties']['area'])
                d[s].append(p['properties']['area'])
    
        
        
        