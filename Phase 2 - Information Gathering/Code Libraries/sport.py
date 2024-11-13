import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import json
from os.path import isfile, join, dirname, exists
from os import makedirs, chdir, listdir
import io
import pandas as pd
import shutil
from geopy.geocoders import Nominatim
from googletrans import Translator
import math
import re

def is_valid_email(email):

    if email is None:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_url(url):

    if url is None:
        return False

    pattern = r'^(https?://)?(www\.)?([a-zA-Z0-9._-]+\.[a-zA-Z]{2,})(/[a-zA-Z0-9._-]*)*$'
    return re.match(pattern, url) is not None

def get_address(lat, lon):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    return location.address if location else None

chdir(dirname(__file__))

df = pd.read_csv(join("../data/standardized/sport", "Sport.csv"))
sports_map = {row.tolist()[1].lower(): row.tolist()[0] for _, row in df.iterrows()}

overpass = "../data/cleaned/overpass-turbo.eu/csv"
comune_trento = "../data/cleaned/comune.trento.it/csv"
paginegialle = "../data/cleaned/paginegialle.it/csv"

overpass_files = sorted(listdir(overpass))
comune_trento_files = sorted(listdir(comune_trento))
paginegialle_files = sorted(listdir(paginegialle))

columns = ["id", "legalName", "openingHours", "telephone", "email", "url", "sports", "location"]

facilities_ids = {}

data = []

# #overpass
for overpass_file in overpass_files:

    df = pd.read_csv(join(overpass, overpass_file))

    for index, row in df.iterrows():

        row = row.tolist()

        legalName = row[0]
        openingHours = row[3]
        telephone = row[4]
        email = row[5]
        url = row[6]

        sports = []

        for sport in row[7].split(";"):

            if sport == "multi":
                continue

            sport_id = sports_map.get(sport)

            if sport_id is None:
                sports_map[sport.capitalize()] = len(sports_map.keys()) + 1

            sports.append(sport_id)
        
        if not len(sports):
            continue

        if legalName not in facilities_ids:
            facilities_ids[legalName] = len(facilities_ids.keys()) + 1

        facility_id = facilities_ids[legalName]

        location = None

        data.append([
            facility_id,
            legalName,
            openingHours,
            telephone,
            email,
            url,
            sports,
            location
        ])

#paginegialle
known_sports = list(sports_map.keys())

for paginegialle_file in paginegialle_files:
    
    df = pd.read_csv(join(paginegialle, paginegialle_file))

    for index, row in df.iterrows():

        row = row.tolist()
        
        legalName = row[0]
        openingHours = row[3]
        telephone = row[4]
        email = row[5]
        url = None
        sports = [] # to be filled
        location = None # to be filled

        if legalName not in facilities_ids:
            facilities_ids[legalName] = len(facilities_ids.keys()) + 1

        facility_id = facilities_ids[legalName]

        data.append([
            facility_id,
            legalName,
            openingHours,
            telephone,
            email,
            url,
            sports,
            location
        ])

#comune.trento
for comune_trento_file in comune_trento_files:
    df = pd.read_csv(join(comune_trento, comune_trento_file))
    df = df.where(pd.notna(df), None)

    for index, row in df.iterrows():

        row = row.tolist()
        
        #legalName,address,email,phone,url,type

        legalName = row[0]
        openingHours = None
        telephone = row[3]
        email = row[2] if is_valid_email(row[2]) else None
        url = row[4] if is_valid_url(row[4]) else None
        sports = [] # to be filled
        location = None # to be filled

        if legalName not in facilities_ids:
            facilities_ids[legalName] = len(facilities_ids.keys()) + 1

        facility_id = facilities_ids[legalName]

        entry = [
            facility_id,
            legalName,
            openingHours,
            telephone,
            email,
            url,
            sports,
            location
        ]
        
        data.append(entry)

df = pd.DataFrame(data=data, columns=columns)
df.to_csv("../data/standardized/sport/SportFacility.csv", index=False, sep=",")

data = []

for sport, sport_id in sports_map.items():
    sport = sport.lower()
    sport = re.sub(r'[^a-zA-Z]', ' ', sport)

    data.append([sport_id, sport])

df = pd.DataFrame(data=data, columns=["id", "name"])
df.to_csv("../data/standardized/sport/Sport.csv", index=False, sep=",")