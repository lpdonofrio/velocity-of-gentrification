# Purpose:
# Create a shapefile containing one single shape for the Manhattan borough and all the neighborhoods of Brooklyn
# And add one single shape for the Brooklyn borough as well

import geopandas as gpd
import pandas as pd


brk = gpd.read_file('nyntas/nynta.shp')
boros = gpd.read_file('boros/boroughs.json')

brk = brk[brk.BoroName == 'Brooklyn']

brk = brk.to_crs(boros.crs)
man = boros[boros.BoroName == 'Manhattan']
brk_one = boros[boros.BoroName == 'Brooklyn']

neighs = brk[['NTAName', 'geometry']]


man['NTAName'] = 'Manhattan'
brk_one['NTAName'] = 'Brooklyn'

neighs = neighs.append(man[['NTAName', 'geometry']])

neighs = neighs.append(brk_one[['NTAName', 'geometry']])

neighs.to_file('locations/final_NTAs_brook.shp')