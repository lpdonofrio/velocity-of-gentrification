import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
import random as rnd
import glob
import time


def select_data(rides, output):
    #create columns identifying start and end point of the rides
    try:
        start_points, end_points, st_man, end_brk = [], [], [], []
        for n, row in rides.iterrows():
            sp = Point((row.pickup_longitude, row.pickup_latitude))
            ep = Point((row.dropoff_longitude, row.dropoff_latitude))
            start_points.append(sp)
            end_points.append(ep)
            
            # test if the ride started in Manhattan 
            st_man.append(neighs[neighs.NTAName == 'Manhattan'].contains(sp) == True)
            
            # test if the ride ended in Brooklyn and get the corresponding NTA
            ntas = neighs[neighs.NTAName != 'Manhattan'].contains(ep)
            try:
                nta = neighs[neighs.NTAName != 'Manhattan'][ntas].NTAName.item()
            except Exception:
                nta = np.NaN
            end_brk.append(nta)
        rides['start_points'] = start_points
        rides['end_points'] = end_points
        rides['st_man'] = st_man
        rides['end_brk'] = end_brk
    
    # exception for 2009 where variable names are different
    except:
        start_points, end_points, st_man, end_brk = [], [], [], []
        for n, row in rides.iterrows():
            sp = Point((row.start_lon, row.start_lat))
            ep = Point((row.end_lon, row.end_lat))
            start_points.append(sp)
            end_points.append(ep)
            # test if the ride started in Manhattan
            st_man.append(neighs[neighs.NTAName == 'Manhattan'].contains(sp) == True)
            
            # test if the ride ended in Brooklyn and get the corresponding NTA
            ntas = neighs[neighs.NTAName != 'Manhattan'].contains(ep)
            try:
                nta = neighs[neighs.NTAName != 'Manhattan'][ntas].NTAName.item()
            except Exception:
                nta = np.NaN
            end_brk.append(nta)
        rides['start_points'] = start_points
        rides['end_points'] = end_points
        rides['st_man'] = st_man
        rides['end_brk'] = end_brk
    
    #subset for end in brooklyn
    rides_end_brk = rides_geo.ix[rides_geo.end_brk.dropna().index]
    
    #subset start in manhattan
    rides_clean = rides_end_brk[rides_end_brk.st_man]
    
    #export CSV file
    rides_clean.to_csv(output)



filenames = glob.glob("/Volumes/LUCIA/NYC Taxi Data/*")



#read in shapefile with relevant locations
neighs = gpd.read_file('locations/final_NTAs.shp')



for filename in filenames:
    t0 = time.time()
    
    # find how many lines are in the csv file and select 1% of it
    n = sum(1 for line in open(filename)) - 1
    s = int(n * 0.01)
    print(time.ctime()+" "+filename+" "+str(s))
    
    # create a new dataframe containing 1% of randomly selected data from the csv file
    skip = sorted(rnd.sample(xrange(1,n+1),n-s))
    df = pd.read_csv(filename, skiprows=skip)
    
    # set lower case variables names
    cols = df.columns
    df.columns = [c.lower() for c in cols]
    
    # save randomly selected 1% of the data as csv file
    df.to_csv("subsets/"+"subset_"+filename[-20:])
    print("df saved.")
    
    # filter the random sample by the start and end location of the rides
    select_data(rides=df, output="rides/"+filename[-20:])
    
    t1 = time.time()
    t = t1-t0
    print("Done in {} secs.".format(t))

