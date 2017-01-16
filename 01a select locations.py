# Purpose:
# Create a shapefile containing one single shape for the Manhattan borough and all the neighborhoods of Brooklyn

import geopandas as gpd
import pandas as pd


brk = gpd.read_file('nyntas/nynta.shp')
boros = gpd.read_file('boros/boroughs.json')

brk = brk[brk.BoroName == 'Brooklyn']

brk = brk.to_crs(boros.crs)
man = boros[boros.BoroName == 'Manhattan']

neighs = brk[['NTAName', 'geometry']]


man['NTAName'] = 'Manhattan'

neighs = neighs.append(man[['NTAName', 'geometry']])


neighs.to_file('locations/final_NTAs.shp')