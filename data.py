import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
from tqdm import tqdm
import pickle
import folium
from folium.plugins import MarkerCluster
from folium.plugins import Search
import matplotlib as mpl
import geopandas 
import copy

print("importing data.py please wait")

trips = pd.read_csv('E:/Sem5/BTP-sem5/gtfs_data/trips.csv')
routes = pd.read_csv('E:/Sem5/BTP-sem5/gtfs_data/routes.csv')
stop_times = pd.read_csv('E:/Sem5/BTP-sem5/gtfs_data/stop_times.csv')
ward_df = geopandas.read_file('E:/Sem5/BTP-sem5/geo_json_files/ward_data.geojson')
ward_df.set_index('Ward_No',inplace=True)


df_of_stop_details=pd.read_csv("E:/Sem5/BTP-sem5/gtfs_data/stops.csv")
df_of_stop_details.set_index('stop_id',inplace=True)
df_of_stop_details= geopandas.GeoDataFrame(df_of_stop_details, geometry=geopandas.points_from_xy(df_of_stop_details.stop_lon, df_of_stop_details.stop_lat),crs="EPSG:4326")

wards={} #konsa stop konse ward mae hai
stops_in_ward={} #kis ward mae konse stops hai

for stop_id in tqdm(df_of_stop_details.index):
    wards[stop_id]=[]

for ward_no in ward_df.index:
    stops_in_ward[ward_no]=[]
    
for stop_id in tqdm(df_of_stop_details.index):
    point=df_of_stop_details.loc[stop_id,'geometry']
    for ward_no in ward_df.index:
        polygon=ward_df.loc[ward_no,'geometry']
        if polygon.contains(point):
            wards[stop_id].append(ward_no)
            stops_in_ward[ward_no].append(stop_id)    

df_of_stop_details['Ward_No']=[np.NaN]*len(df_of_stop_details)
counter=0
for stop_id in wards:
    if(len(wards[stop_id])>0):
        df_of_stop_details.loc[stop_id,'Ward_No']=wards[stop_id][0]
    else:
        counter+=1
count_of_stops=df_of_stop_details.groupby(['Ward_No']).stop_name.agg(['count'])

num_stops=[]
for ward in ward_df.index:
    try: 
        number_of_stops_in_a_ward=count_of_stops.loc[ward].values[0]
    except:
        number_of_stops_in_a_ward=0
    num_stops.append(number_of_stops_in_a_ward)
# print(num_stops)
ward_df['num_of_stops']=num_stops

# Number of trips corresponding to every route and first trip of every route used for indexing later
route_trips = {}
route_trip_ind = {}

x = trips.groupby('route_id')

for i in x.groups:
    ls = list(x.get_group(i)['trip_id'])
    route_trips[i] =len(ls)
    if len(ls) == 0:
        route_trip_ind[i] = -1
    else:
        route_trip_ind[i] = ls[0]

        
# Connectivity of each stop with every other stop in terms of total number of trips in a day from s1 to s2
initial_score = {}

for i in tqdm(df_of_stop_details.index):
    for j in df_of_stop_details.index:
        if i != j:
            initial_score[(i, j)] = 0
            
y = stop_times.groupby('trip_id')

for i in tqdm(x.groups):
    curr_trip = route_trip_ind[i]
    curr_stops=list(y.get_group(curr_trip)['stop_id'])
    for in1 in range(len(curr_stops)):
        for in2 in range(in1 + 1, len(curr_stops)):
            s1=curr_stops[in1]
            s2=curr_stops[in2]
            if(s1==s2):
                continue
            initial_score[(s1, s2)] += route_trips[i]


# Connectivity ward and calculating it's score with every other ward
max_score=0

score={}
for pward in tqdm(ward_df.index):
    t_dict={}
    for ward in ward_df.index:
        if pward==ward:
            t_dict[ward]=0
            continue
        # if there are no stops in pward or ward
        if len(stops_in_ward[pward])==0 or len(stops_in_ward[ward])==0:
            t_dict[ward]=0
            continue
        curr=0
        
        for s1 in stops_in_ward[pward]:
            for s2 in stops_in_ward[ward]:
                if(s1==s2):
                    continue
                curr += initial_score[(s1, s2)]
        curr=curr/len(stops_in_ward[pward])
        curr=curr/len(stops_in_ward[ward])
        max_score=max(max_score,curr)
        t_dict[ward]=curr
    score[pward]=t_dict
        
print("data.py imported succesfully")


# pickle.dump(score,open("score_delhi.pkl",'wb'))
