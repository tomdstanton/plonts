#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pandas import DataFrame
from requests import get
from datetime import datetime
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import urllib.parse

api_keys = {"trefle": "Fl172rMx2vXJDhRa6MYesqIvACkibM-kZ0JzOEtRPvA",
            "plantnet": "2b10GOhutBEPgPOOZKAsVtygyO",
            "owm": "b5608072b03d5196b9c9942fb2dc4cb0"}


def fetch(url, site):
    return get(url, headers={'Authorization': f'Bearer {api_keys[site]}'}).json()


# Query trefle api with plant name
query = "Garden strawberry"
trefle_search = fetch(f'https://trefle.io/api/v1/plants/search?q={query}', "trefle")
if len(trefle_search['data']) == 0:
    print("No results found")
else:
    # Put in dataframe and print for developing - remove later
    query_df = pd.DataFrame(trefle_search['data'])
    print(query_df[['common_name', 'slug']].to_markdown(index=False))

# Fetch the 'species' data for first result based on dataframe 'slug' column
trefle_result = fetch(f'https://trefle.io/api/v1/species/{query_df.slug[0]}', "trefle")

# Open Image from first result
photo = get(trefle_result['data']['image_url'], stream=True)
photo.raw.decode_content = True
image = Image.open(photo.raw)
plt.imshow(image)

# Variables from growth data dict
grw = trefle_result['data']['growth']
description = grw['description']
sowing = grw['sowing']
min_temp = grw['minimum_temperature']['deg_c']
max_temp = grw['maximum_temperature']['deg_c']
light = grw['light']
atm_hum = grw['atmospheric_humidity']

print(grw)

# Fetch latitude and longitude from postcode
postcode = 'EH93ED'
if ' ' not in postcode:
    postcode = postcode[:-3] + ' ' + postcode[-3:]
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(postcode) + '?format=json'
location = get(url).json()
lat = location[0]["lat"]
lon = location[0]["lon"]

# Get weather for location from OpenWeatherMap
url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_keys["owm"]}'
owm = get(url).json()
place = owm["name"]
country = owm["sys"]["country"]
weather_main = owm["weather"][0]["main"]
weather_desc = owm["weather"][0]["description"]
temp_main = int(owm["main"]["temp"] - 273.15)
humidity = owm["main"]["humidity"]
wind_speed = int(owm["wind"]["speed"])
wind_temp = int(owm["wind"]["deg"] - 273.15)
sunrise = datetime.fromtimestamp(owm["sys"]["sunrise"]).strftime("%X")
sunset = datetime.fromtimestamp(owm["sys"]["sunset"]).strftime("%X")
light_hours = datetime.fromtimestamp(owm["sys"]["sunset"]-owm["sys"]["sunrise"]).strftime("%X")

print(f'Right now in {place} ({country})')
print(f'Weather: {weather_main} - {weather_desc}')
print(f'Temperature: {temp_main}°C with {humidity}% humidity')
print(f'Weather: {weather_main} - {weather_desc}')
print(f'Wind: {wind_speed}mph and {wind_temp}°C')

wind_speed = int(owm["wind"]["speed"])
wind_temp = int(owm["wind"]["deg"] - 273.15)
sunrise = datetime.fromtimestamp(owm["sys"]["sunrise"]).strftime("%X")
sunset = datetime.fromtimestamp(owm["sys"]["sunset"]).strftime("%X")
light_hours = datetime.fromtimestamp(owm["sys"]["sunset"]-owm["sys"]["sunrise"]).strftime("%X")



# Find native plants to your location
# country = location[0]["display_name"].rsplit(', ', 1)[1]
# native_plants = fetch(
#     f'https://trefle.io/api/v1/distributions/'
#     f'{country}/plants', "trefle")
