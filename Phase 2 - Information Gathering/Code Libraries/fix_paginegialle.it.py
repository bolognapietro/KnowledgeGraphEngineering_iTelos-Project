import pandas as pd
import os
from os.path import join
import math
import json

df_location = pd.read_csv(r"C:\Users\sassi\Desktop\knowledge-graph-engineering-project\Phase 2 - Information Gathering\data\standardized\location\Location.csv")
dict_location = {}

for _, item in df_location.iterrows():
    item = item.tolist()
    dict_location[(item[1], item[2])] = item[0]

df_sport_facility = pd.read_csv(r"C:\Users\sassi\Desktop\knowledge-graph-engineering-project\Phase 2 - Information Gathering\data\standardized\sport\SportFacility.csv")
dict_sport_facility = {}

new_rows = []

for index, item in df_sport_facility.iterrows():

    item = item.tolist()

    if index < 1765:
        new_rows.append(item)
        continue
    
    key = (item[1], item[3])

    dict_sport_facility[key] = index

directory = r"C:\Users\sassi\Desktop\knowledge-graph-engineering-project\Phase 2 - Information Gathering\data\cleaned\paginegialle.it\csv"

with open(r"C:\Users\sassi\Desktop\knowledge-graph-engineering-project\Phase 2 - Information Gathering\Code Libraries\sport_map.json", "r", encoding="utf-8") as f:
    sports = json.loads(f.read())

for f in os.listdir(directory):

    f = join(directory, f)

    if not f.endswith(".csv"):
        continue

    df = pd.read_csv(f)

    for _, row in df.iterrows():
        row = row.tolist()

        location_id = dict_location.get((row[1], row[2]))

        if location_id is None:
            continue #! missing location
        
        key = (row[0], row[4])
        index = dict_sport_facility.get(key)

        if index is None:
            key = (row[0], row[4][1:])
            index = dict_sport_facility[key]

        new_row = df_sport_facility.loc[index, :].tolist()[:-1]
        new_row.append(int(location_id))

        new_row = new_row[:3] + [row[4]] + new_row[4:]

        legalName = new_row[1].lower()

        matched_sports = []

        for key, item in sports.items():

            if any(keyword.lower() in legalName for keyword in item["keywords"]):
                matched_sports.append(str(item["id"]))

        new_row = new_row[:6] + [",".join(matched_sports)] + new_row[7:]

        new_rows.append(new_row)

new_df = pd.DataFrame(new_rows, columns=df_sport_facility.columns)
new_df.to_csv(r"C:\Users\sassi\Desktop\knowledge-graph-engineering-project\Phase 2 - Information Gathering\data\standardized\sport\SportFacility.csv", index=False)
