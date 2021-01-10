#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from requests import get
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import urllib.parse

parser = ArgumentParser(add_help=False, usage="", description="")
parser.add_argument('postcode', default='EH93ED')
parser.add_argument('query', default='')

token = "Fl172rMx2vXJDhRa6MYesqIvACkibM-kZ0JzOEtRPvA"
place = "?"
species = "?"
genus = "?"
plants = "?"
query = "daisy"

header = "https://trefle.io/api/v1/"

url = f'{header}plants/search?q={query}'
r = get(url, headers={'Authorization': f'Bearer {token}'}).json()

if len(r['data']) == 0:
      print("No results found")
else:
      df = pd.DataFrame(r['data'])
      print(df[['common_name', 'slug']].to_markdown(index=False))

url = f'{header}plants/{df.slug[0]}'
r = get(url, headers={'Authorization': f'Bearer {token}'}).json()


# Open Image from first result
r = get(df.image_url[0], stream=True)
r.raw.decode_content = True
image = Image.open(r.raw)
plt.imshow(image)
plt.show()

# Fetch latitude and longitude from postcode

url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(postcode) +'?format=json'
r = get(url).json()
lat = r[0]["lat"]
lon = r[0]["lon"]

# Get weather for location
owm_api_key = "b5608072b03d5196b9c9942fb2dc4cb0"
url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={owm_api_key}'
print(url)
r = get(url).json()
