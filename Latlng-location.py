#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 17:23:56 2019
 
 
 
import pandas as pd, requests, logging, time
 
lfh = logging.FileHandler('reverse_geocoder.log', mode='w', encoding='utf-8')
lfh.setFormatter(logging.Formatter('%(levelname)s %(asctime)s %(message)s'))
log = logging.getLogger('reverse_geocoder')
log.setLevel(logging.INFO)
log.addHandler(lfh)
log.info('process started')
 
df = pd.read_csv('radiation_usa.csv', encoding='utf-8', names=["time", "lat", "long", "value"])
df['geocode_data'] = ''
df['county'] = ''
df['state'] = ''
df['country'] = ''
 
print(df[:5])
 
 
api_key = "xxxxxxx-xxxxxx" # Use your own api_key
 
 
def reverse_geocode(latlng):
    time.sleep(0.1)
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={}' + "&key={}".format(api_key)
    request = url.format(latlng)
    log.info(request)
    response = requests.get(request)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]
 
df['latlng'] = df.apply(lambda row: '{},{}'.format(row['lat'], row['long']), axis=1)
df['geocode_data'] = df['latlng'].map(reverse_geocode)
 
print(df[:5])
 
def parse_county(geocode_data):
    if (not geocode_data is None) and ('address_components' in geocode_data):
        for component in geocode_data['address_components']:
            if 'administrative_area_level_2' in component['types']:
                return component['long_name']
    return None
 
 
def parse_state(geocode_data):
    if (not geocode_data is None) and ('address_components' in geocode_data):
        for component in geocode_data['address_components']:
            if 'administrative_area_level_1' in component['types']:
                return component['long_name']
    return None
 
 
def parse_country(geocode_data):
    if (not geocode_data is None) and ('address_components' in geocode_data):
        for component in geocode_data['address_components']:
            if 'country' in component['types']:
                return component['long_name']
    return None
 
 
df['county'] = df['geocode_data'].map(parse_county)
df['state'] = df['geocode_data'].map(parse_state)
df['country'] = df['geocode_data'].map(parse_country)
 
print(len(df))
print(df[:5])
 
df.to_csv('radiation_city_usa.csv', encoding='utf-8', index=False)
