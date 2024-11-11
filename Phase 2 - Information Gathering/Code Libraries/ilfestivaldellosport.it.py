import requests
from bs4 import BeautifulSoup
import re
import json
from os.path import join, dirname, exists
from os import makedirs, chdir
import shutil
import pandas as pd

from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'it_IT')

chdir(dirname(__file__))

ROOT: str = "../data/raw/ilfestivaldellosport.it"
ROOT_JSON = join(ROOT, "json")
ROOT_CSV = join(ROOT, "csv")

if exists(ROOT):
    shutil.rmtree(ROOT)

makedirs(ROOT, exist_ok=True)
makedirs(ROOT_JSON, exist_ok=True)
makedirs(ROOT_CSV, exist_ok=True)

url = f"https://www.ilfestivaldellosport.it/programma/"

response = requests.get(url=url)
soup = BeautifulSoup(response.content, "html.parser")

year = re.search(r'/(\d{4})/', soup.find("a", {"title": {"Programma"}}).attrs["href"]).group(1)

sports = soup.find("div", {"class": "form-group field-programmafilter-sport"})
sports = sports.find_all("option")
sports = {sport.text: {"value": sport.attrs["value"], "events": []} for sport in sports}

sports_csv = []

locations = {}

base_url = f"https://www.ilfestivaldellosport.it/programma/?ProgrammaFilter[sport][]="

for index1, (sport_name, sport_info) in enumerate(sports.items()):

    url = f"{base_url}{sport_info['value']}"

    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")

    events = soup.find_all("div", {"class": "evento-box"})
    
    for index2, event in enumerate(events):

        print(f" "*100, end="\r")
        print(f"[{index1 + 1} / {len(sports)}] {sport_name}: {index2 + 1} / {len(events)}", end="\r")

        url = event.find("a").attrs["href"]
        url = f"https://www.ilfestivaldellosport.it{url}"

        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        name = soup.find("div", {"class": "event-title-container"}).text.strip()

        for sport in sports:
            name = name.replace(sport, "")

        name = re.sub(r'\n+', '\n', name).strip()
        name = re.sub(r'\t+', '', name).strip()
        name = re.sub(r'[^\x00-\x7F]+', '', name)

        info = soup.find("section", {"class": "event-info-container"})
        info = info.find_all("div", {"class": "info-icon"})
        
        when_day, when_hours = info[1].text.strip().split("-")
        when_day = f"{when_day.strip()} {year}"
        when_hours = when_hours.strip()
        when = f"{when_day} {when_hours}"
        date = datetime.strptime(when, "%A %d %B %Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")

        guests = soup.find("div", {"class": "section-ospiti-evento"})

        if guests is not None:
            guests = guests.find_all("div", {"class": "ospiti-box"})
            guests = [guest.find("p").text.strip() for guest in guests]

        else:
            guests = []

        location = info[0].text.strip()
        location = re.sub(r'\n+', '', location).strip()
        location = re.sub(r'\t+', '', location).strip()
        location = re.sub(r'[^\x00-\x7F]+', '', location)

        if location not in locations:

            url = info[0].find("a").attrs["href"]
            url = f"https://www.ilfestivaldellosport.it{url}"

            response = requests.get(url=url)
            soup = BeautifulSoup(response.content, "html.parser")

            address = soup.find("div", {"class": "info-icon"}).text.strip()

            locations[location] = {
                "name": location,
                "address": address
            }

            location = locations[location]

        else:
            location = locations[location]

        sports[sport_name]["events"].append({
            "name": name,
            "location": location,
            "date": date,
            "guests": guests
        })

        sports_csv.append([
            sport_name,
            name,
            location,
            date,
            guests
        ])
    
with open(join(ROOT_JSON, "ilfestivaldellosport.it.json"), "w+", encoding="utf-8") as f:
    f.write(json.dumps(sports, indent=4))

df = pd.DataFrame(data=sports_csv, columns=["sport", "name", "location", "date", "guests"])
df.to_csv(join(ROOT_CSV, "ilfestivaldellosport.it.csv"), index=False, sep=",")