import os, rasterio

ruta = r'E:\CUBAFINAL\masks'
ruta_slope = r'E:\CUBAFINAL\mask_'

#Hacemos la lista de los rasters con la suma de las 3 clasificaciones
lsuma = [os.path.join(ruta, i) for i in os.listdir(ruta) if i.endswith('.tif') and i.startswith('suma')]
lslope = [os.path.join(ruta_slope, i) for i in os.listdir(ruta_slope) if i.endswith('.tif') and 'slope' in i]
#Hacemos un diccionario con las clasificaciones y las pendientes de cada cuadricula
d = dict(zip(lsuma, lslope))

for n in range(1,4):
    
    print('Clase', n)
    #vamos abriendo los rasters de suma y pendiente
    for k, v in d.items():

        with rasterio.open(k) as suma:
            SUMA = suma.read()
        with rasterio.open(v) as slope:
            SLOPE = slope.read()
        #Class1
        P5 = SUMA[(SUMA==n) & (SLOPE == 1)]
        P10 = SUMA[(SUMA==n) & (SLOPE == 2)]
        P20 = SUMA[(SUMA==n) & (SLOPE == 3)]
        P30 = SUMA[(SUMA==n) & (SLOPE == 4)]
        P100 = SUMA[(SUMA==n) & (SLOPE == 5)]

        total = P5.size + P10.size + P20.size + P30.size + P100.size

        print('\t', k, P5.size * 900 /10000, 'ha |', round(P5.size * 100 / total, 2), '%')
        print('\t', k, P10.size * 900 /10000, 'ha |', round(P10.size * 100 / total, 2), '%')
        print('\t', k, P20.size * 900 /10000, 'ha |', round(P20.size * 100 / total, 2), '%')
        print('\t', k, P30.size * 900 /10000, 'ha |', round(P30.size * 100 / total, 2), '%')
        print('\t', k, P100.size * 900 /10000, 'ha |', round(P100.size * 100 / total, 2), '%', '\n')
        