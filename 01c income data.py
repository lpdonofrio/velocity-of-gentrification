# Purpose:
# Create shapefiles with 2009 and 2013 median income data

import geopandas as gpd
import pandas as pd


tracts = gpd.read_file('tract_shp/cb_2013_36_tract_500k.shp')
income_2009 = pd.read_csv('income/income_2009.csv')
income_2013 = pd.read_csv('income/income_2013.csv')

equivalence = pd.read_csv('tract_NTA/brooklyn_equiv.csv')

tracts.GEOID = tracts.GEOID.astype(int)

merged_2009 = pd.merge(left=tracts, right=income_2009, how='left', left_on='GEOID', right_on='GEOID')
merged_all = pd.merge(left=merged_2009, right=income_2013, how='left', left_on='GEOID', right_on='GEOID')
merged_all.TRACTCE = merged_all.TRACTCE.astype(int)
merged_nta = pd.merge(left=merged_all, right=equivalence, how='left', left_on='TRACTCE', right_on='TRACTCE')

# Shapefile at the census tract level
merged_nta.to_file('tract_shp/tracts_income.shp')


# Group income data by NTA
nta_income = merged_nta[merged_nta.COUNTYFP == '047']
nta_income = nta_income.dropna()
nta_income.median_09 = nta_income.median_09.astype(int)
nta_income = nta_income.groupby('NTA_code')['median_09', 'median_13'].mean().reset_index()

# Add coordinates for NTAs
nta_shapes = gpd.read_file('nyntas/nynta.shp')
nta_shapes = nta_shapes[nta_shapes.BoroName == 'Brooklyn']
merged_income_nta = pd.merge(left=nta_shapes, right=nta_income, how='left', left_on='NTACode', right_on='NTA_code')

# Shapefile at the NTA level
merged_income_nta.to_file('income/income_ntas.shp')