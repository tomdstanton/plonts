#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pandas import DataFrame
from requests import get
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import urllib.parse

api_keys = {"trefle": "Fl172rMx2vXJDhRa6MYesqIvACkibM-kZ0JzOEtRPvA",
            "plantnet": "2b10GOhutBEPgPOOZKAsVtygyO",
            "owm": "b5608072b03d5196b9c9942fb2dc4cb0"}


def fetch(url, site):
    return get(url, headers={'Authorization': f'Bearer {api_keys[site]}'}).json()


query = "daisy"
postcode = 'EH93ED'

r = fetch(f'https://trefle.io/api/v1/plants/search?q={query}', "trefle")
if len(r['data']) == 0:
    print("No results found")
else:
    df: DataFrame = pd.DataFrame(r['data'])
    print(df[['common_name', 'slug']].to_markdown(index=False))

r = fetch(f'https://trefle.io/api/v1/plants/{df.slug[0]}', "trefle")

# Open Image from first result
r = get(df.image_url[0], stream=True)
r.raw.decode_content = True
image = Image.open(r.raw)
plt.imshow(image)
plt.show()

# Fetch latitude and longitude from postcode
if ' ' not in postcode:
      postcode = postcode[:-3] + ' ' + postcode[-3:]

url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(postcode) + '?format=json'
r = get(url).json()
lat = r[0]["lat"]
lon = r[0]["lon"]

# Get weather for location
r = fetch(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}', "owm")
