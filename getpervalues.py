
for k, v in d.items():
    
    with rasterio.open(v[0]) as l2014:
        LDST2014 = l2014.read()
        LDST2014_M = LDST2014[(LDST2014 == 1)]
        POR_LDST2014_M = (((LDST2014_M.size * 900) * 100)/ v[-1]) 
        print(k, 'L82014', POR_LDST2014_M)
        
    with rasterio.open(v[1]) as  l2016:
        LDST2016 = l2016.read()
        LDST2016_M = LDST2016[(LDST2016 == 2)]
        POR_LDST2016_M = (((LDST2016_M.size * 900)* 100) / v[-1]) 
        print(k, 'L82016', POR_LDST2016_M)
                
    with rasterio.open(v[2]) as  s2:
        S2A = s2.read()
        S2A_M = S2A[(S2A == 1)]
        POR_S2A_M = (((S2A_M.size * 900) * 100)/ v[-1]) 
        print(k, 'S2A', POR_S2A_M)
        print('-----------------')
        
    with rasterio.open(v[3]) as l2014CM:
        LDST2014CM = l2014CM.read()
        LDST2014_NB = LDST2014CM[(LDST2014CM == 1)]
        POR_LDST2014_NB = (((LDST2014_NB.size * 900) * 100) / v[-1]) 
        print(v[3], ' Porcentaje de nubes en L82014', POR_LDST2014_NB)
        
    with rasterio.open(v[4]) as  l2016B1:
        LDST2016B1 = l2016B1.read()
        LDST2016_NB = LDST2016B1[(LDST2016B1 == 1)]
        POR_LDST2016_NB = (((LDST2016_NB.size * 900)* 100) / v[-1]) 
        print(v[4], ' Porcentaje de nubes en L82016', POR_LDST2016_NB)
    
    with rasterio.open(v[5]) as  s2cm:
        S2CM = s2cm.read()
        S2A_NB = S2CM[(S2CM == 1)]
        POR_S2A_NB = (((S2A_NB.size * 900) * 100)/ v[-1]) 
        print(v[5], ' Porcentaje de nubes en Sentinel 2', POR_S2A_NB)
        
    #comunL8:
    comunLandsat = LDST2014[(LDST2014 == 1) & (LDST2016 == 2)]
    CLANDSAT = comunLandsat.size * 900
    totallandsat = (LDST2014_M.size + LDST2016_M.size) * 900 #esto seria el total en el que en cualquiera de los 2 es mrbu
    #print((comunLandsat.size * 900) / totallandsat* 100)
    print('L82014 que es Marabu en L82016:', (CLANDSAT / (LDST2014_M.size * 900)) * 100)
    print('L82016 que es Marabu en L82014:', (CLANDSAT / (LDST2016_M.size * 900)) * 100)
    print('Comun sobre el total de los 2:', (CLANDSAT / totallandsat) * 100)
    #print(((comunLandsat2016.size * 900) / v[3]) * 100)
    comunl82014_s2a = LDST2014[(LDST2014 == 1) & (S2A == 1)]
    CL2014S2A = comunl82014_s2a.size * 900
    print('L82014 que es Marabu en Sentinel2:', (CL2014S2A / (LDST2014_M.size * 900)) * 100)
    comunl82016_s2a = LDST2014[(LDST2016 == 2) & (S2A == 1)]
    CL2016S2A = comunl82016_s2a.size * 900
    print('L82016 que es Marabu en Sentinel2:', (CL2016S2A / (LDST2016_M.size * 900)) * 100)
    print('-----------------')
    print('Contando con las nubes:\n')
    #Porcentaje de L82014Marabu que son nubes en L82016
    
    #hacemos landsat 2014 con landsat 2016
    L2014CFREE = LDST2014[(LDST2014CM != 1) & (LDST2016B1 != 1)]
    L2016CFREE = LDST2016[(LDST2014CM != 1) & (LDST2016B1 != 1)]
    
    LDST2014_MFREE = L2014CFREE[(L2014CFREE == 1)]
    LDST2016_MFREE = L2016CFREE[(L2016CFREE == 2)]
    
    ###############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!LANDSAT SOLO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    comunLandsatfree = L2014CFREE[(L2014CFREE == 1) & (L2016CFREE == 2)]
    CLANDSATFREE = comunLandsatfree.size * 900
    totallandsatfree = (LDST2014_M.size + LDST2016_M.size) * 900 #esto seria el total en el que en cualquiera de los 2 es mrbu
    #print((comunLandsat.size * 900) / totallandsat* 100)
    print('L82014 que es Marabu en L82016:', (CLANDSATFREE / (LDST2014_MFREE.size * 900)) * 100)
    print('L82016 que es Marabu en L82014:', (CLANDSATFREE / (LDST2016_MFREE.size * 900)) * 100)
    print('Comun sobre el total de los 2:', (CLANDSATFREE / totallandsatfree) * 100)
    
    #hacemos landsat 2014 con sentinel 2
    S2AFREE = S2A[(LDST2014CM != 1) & (S2CM != 1)]
    L2014S2FREE = LDST2014[(LDST2014CM != 1) & (S2CM != 1)]
    
    LDST2014S2_MFREE = L2014S2FREE[(L2014S2FREE == 1)]
    S2A_MFREE = S2AFREE[(S2AFREE == 1)]
    
    
    ###############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!LANDSAT Y SENTINEL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    comunLandsats2afree = L2014S2FREE[(L2014S2FREE == 1) & (S2AFREE == 1)]
    CLANDSATS2AFREE = comunLandsats2afree.size * 900
    totallandsats2afree = (LDST2014S2_MFREE.size + S2A_MFREE.size) * 900 #esto seria el total en el que en cualquiera de los 2 es mrbu
    #print((comunLandsat.size * 900) / totallandsat* 100)
    print('--------------\nL82014 que es Marabu en S2:', (CLANDSATS2AFREE / (LDST2014S2_MFREE.size * 900)) * 100)
    print('S2 que es Marabu en L82014:', (CLANDSATS2AFREE / (S2A_MFREE.size * 900)) * 100)
    print('Comun sobre el total de los 2:', (CLANDSATS2AFREE / totallandsats2afree) * 100)
    
    #hacemos landsat 2016 con sentinel 2
    S2AFREEL82016 = S2A[(LDST2016B1 != 1) & (S2CM != 1)]
    L2016S2FREE = LDST2016[(LDST2016B1 != 1) & (S2CM != 1)]
    
    LDST2016S2_MFREE = L2016S2FREE[(L2016S2FREE == 2)]
    S2AL82016_MFREE = S2AFREEL82016[(S2AFREEL82016 == 1)]
    
    
    ###############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!LANDSAT Y SENTINEL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    comunLandsats2a_free = L2016S2FREE[(L2016S2FREE == 2) & (S2AFREEL82016 == 1)]
    CLANDSATS2_AFREE = comunLandsats2a_free.size * 900
    totallandsats2a_free = (LDST2016S2_MFREE.size + S2AL82016_MFREE.size) * 900 #esto seria el total en el que en cualquiera de los 2 es mrbu
    #print((comunLandsat.size * 900) / totallandsat* 100)
    print('--------------\nL82016 que es Marabu en S2:', (CLANDSATS2_AFREE / (LDST2016S2_MFREE.size * 900)) * 100)
    print('S2 que es Marabu en L82016:', (CLANDSATS2_AFREE / (S2AL82016_MFREE.size * 900)) * 100)
    print('Comun sobre el total de los 2:', (CLANDSATS2_AFREE / totallandsats2a_free) * 100)
    
    
    
    
    print('\n++++++++++++++++\n')
    
#def comun(r1, r2):
    
    