import json

from os.path import isfile, join, dirname, exists
from os import makedirs, chdir

import pandas as pd

import numpy as np

chdir(dirname(__file__))

ROOT: str = "../data/raw/overpass-turbo.eu"
ROOT_JSON = join(ROOT, "json")
ROOT_CSV = join(ROOT, "csv")

with open(join(ROOT_JSON, "overpass-turbo.eu.json"), "r", encoding="utf-8") as f:
    data = json.loads(f.read())

rows = []

features = data["features"]

facilities = []

for feature in features:
    properties = feature["properties"]

    sport = properties.get("sport", "multi")

    if sport == "multi":
        continue

    name = properties.get("name")
    open_hours = properties.get("opening_hours")
    phone_number = properties.get("phone")
    email = properties.get("email")
    website = properties.get("website")
    price = properties.get("price")

    flat_coords = []

    coordinates = feature["geometry"]["coordinates"]

    if len(coordinates) == 2 and all(not isinstance(item, list) for item in coordinates):
        flat_coords = [coordinates]

    else:
        for item in coordinates:

            if isinstance(item, list):
                flat_coords.extend(item)
            
            else:
                flat_coords.append(item)

    coords_array = np.array(flat_coords)

    centroid_lat = coords_array[:, 1].mean()
    centroid_lon = coords_array[:, 0].mean()

    facilities.append({
        "legalName": name,
        "lat": centroid_lat,
        "lon": centroid_lon,
        "openingHours": open_hours,
        "telephone": phone_number,
        "email": email,
        "url": website,
        "sport": sport
    })

    rows.append([name, centroid_lat, centroid_lon, open_hours, phone_number, email, website, sport])

df = pd.DataFrame(data=rows, columns=list(facilities[0].keys()))
df.to_csv(join(ROOT_CSV, "overpass-turbo.eu.csv"), index=False, sep=",")



