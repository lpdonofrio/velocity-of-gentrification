# Purpose:
# Create shapefiles with 2009 and 2013 rent data

import geopandas as gpd
import pandas as pd


tracts = gpd.read_file('tract_shp/cb_2013_36_tract_500k.shp')
rent_2009 = pd.read_csv('rent/gross_rent_2009.csv')
rent_2013 = pd.read_csv('rent/gross_rent_2013.csv')
perc_income_2009 = pd.read_csv('rent/perc_income_2009.csv')
perc_income_2013 = pd.read_csv('rent/perc_income_2013.csv')

equivalence = pd.read_csv('tract_NTA/brooklyn_equiv.csv')

tracts.GEOID = tracts.GEOID.astype(int)

merged_rent_2009 = pd.merge(left=tracts, right=rent_2009, how='left', left_on='GEOID', right_on='GEOID')
merged_rent_2013 = pd.merge(left=merged_rent_2009, right=rent_2013, how='left', left_on='GEOID', right_on='GEOID')
merged_2009 = pd.merge(left=merged_rent_2013, right=perc_income_2009, how='left', left_on='GEOID', right_on='GEOID')
merged_2013 = pd.merge(left=merged_2009, right=perc_income_2013, how='left', left_on='GEOID', right_on='GEOID')
merged_2013.TRACTCE = merged_2013.TRACTCE.astype(int)
merged_nta = pd.merge(left=merged_2013, right=equivalence, how='left', left_on='TRACTCE', right_on='TRACTCE')

# Shapefile at the census tract level
merged_nta.to_file('tract_shp/tracts_rent.shp')


# Group income data by NTA
nta_rent = merged_nta[merged_nta.COUNTYFP == '047']
nta_rent = nta_rent.dropna()
nta_rent = nta_rent.groupby('NTA_code')['rent_09', 'rent_13', 'perc_09', 'perc_13'].mean().reset_index()

# Add coordinates for NTAs
nta_shapes = gpd.read_file('nyntas/nynta.shp')
nta_shapes = nta_shapes[nta_shapes.BoroName == 'Brooklyn']
merged_rent_nta = pd.merge(left=nta_shapes, right=nta_rent, how='left', left_on='NTACode', right_on='NTA_code')

# Shapefile at the NTA level
merged_rent_nta.to_file('rent/rent_ntas.shp')
