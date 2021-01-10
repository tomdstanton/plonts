#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import requests
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# if __name__ == "__main__":
#     parser = ArgumentParser(add_help=False, usage="", description="")
#
#     parser.add_argument('input', nargs='*', default=['-'])

token = "Fl172rMx2vXJDhRa6MYesqIvACkibM-kZ0JzOEtRPvA"
place = "?"
species = "?"
genus = "?"
plants = "?"
text_query = "tomato"

url = f'https://trefle.io/api/v1/' \
      f'species/search?q={text_query}' \
      f'&token={token}'

print(url)

r = requests.get(url).json()

df = pd.DataFrame(r['data'])

response = requests.get(df.image_url[0], stream=True)
response.raw.decode_content = True
image = Image.open(response.raw)
plt.imshow(image)
plt.show()
