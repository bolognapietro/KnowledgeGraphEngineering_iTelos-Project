import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import json
from os.path import isfile, join, dirname
from os import makedirs, chdir
import io
import pandas as pd
import shutil

chdir(dirname(__file__))

ROOT: str = "../data/raw/comune.trento.it"
ROOT_JSON = join(ROOT, "json")
ROOT_CSV = join(ROOT, "csv")

#shutil.rmtree(ROOT)

makedirs(ROOT, exist_ok=True)
makedirs(ROOT_JSON, exist_ok=True)
makedirs(ROOT_CSV, exist_ok=True)

facilities = {
    "impianti_ad_accesso_libero": [],
    "impianti_gestiti_da_asis": []
}

details_map = {
    "indirizzo": "address",
    "email": "email",
    "indirizzo web": "website",
    "telefono": "phone",
    "tipologia di luogo": "type"
}

def impianti_ad_accesso_libero():

    results_json = []
    results_csv = []

    url = "https://www.comune.trento.it/Aree-tematiche/Sport/Impianti-sportivi/Impianti-ad-accesso-libero"

    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")

    categories = soup.find_all("div", {"class": "class-luogo media"})

    for index1, category in enumerate(categories):

        url = category.find("a").attrs["href"]
        url = "https://www.comune.trento.it" + url
        
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")

        items = soup.find("div",{"class": "content-main full-stack"}).find_all("li")

        for index2, item in enumerate(items):
            
            url = item.find("a").attrs["href"]

            if url == "#":
                continue

            url = "https://www.comune.trento.it" + url

            response = requests.get(url=url)
            soup = BeautifulSoup(response.content, "html.parser")

            name = soup.find("div", {"class": "content-title"}).text.strip()
            name = re.sub(r'\n+', ' ', name)

            print(" "*100, end="\r")
            print(f"[{index1 + 1} / {len(categories)}][{index2 + 1} / {len(items)}] {name}", end="\r")

            description = soup.find("div", {"class": "media"}).text.strip()
            description = re.sub(r'\n+', '\n', description)

            details = soup.find("div", {"class": "content-detail"}).find_all("div", {"class": "row"})
            details_json = {}

            for detail in details:
                detail_key = detail.find("div", {"class": "col-md-3"})
                detail_key = detail_key.text.strip().lower()

                detail_value = detail.find("div", {"class": "col-md-9"})
                detail_value = detail_value.text.strip().lower()

                key = details_map.get(detail_key)

                if key is None:
                    continue

                details_json[key] = detail_value
            
            entry = {
                "name": name,
                "description": description
            }

            entry.update(details_json)

            if entry in results_json:
                continue

            results_json.append(entry)
            results_csv.append([value for value in entry.values()])

    with open(join(ROOT_JSON, "impianti_ad_accesso_libero.json"), "w+", encoding="utf-8") as f:
        f.write(json.dumps(results_json, indent=4))

    df = pd.DataFrame(data=results_csv, columns=list(results_json[0].keys()))
    df.to_csv(join(ROOT_CSV, "impianti_ad_accesso_libero.csv"), index=False, sep=";")

def impianti_gestiti_da_asis():

    results_json = []
    results_csv = []

    url = "https://www.comune.trento.it/Aree-tematiche/Sport/Impianti-sportivi/Impianti-gestiti-da-Asis"

    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")

    items = soup.find_all("div", {"class": "class-luogo media"})

    for index1, item in enumerate(items):

        url = item.find("a").attrs["href"]
        url = "https://www.comune.trento.it" + url
        
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")

        name = soup.find("div", {"class": "content-title"}).text.strip()
        name = re.sub(r'\n+', ' ', name)

        print(" "*100, end="\r")
        print(f"[{index1 + 1} / {len(items)}] {name}", end="\r")

        description = soup.find("div", {"class": "media"}).text.strip()
        description = re.sub(r'\n+', '\n', description)

        details = soup.find("div", {"class": "content-detail"}).find_all("div", {"class": "row"})
        details_json = {}

        for detail in details:
            detail_key = detail.find("div", {"class": "col-md-3"})
            detail_key = detail_key.text.strip().lower()

            detail_value = detail.find("div", {"class": "col-md-9"})
            detail_value = detail_value.text.strip().lower()

            key = details_map.get(detail_key)

            if key is None:
                continue

            details_json[key] = detail_value
        
        entry = {
            "name": name,
            "description": description
        }

        entry.update(details_json)

        if entry in results_json:
            continue

        results_json.append(entry)
        results_csv.append([value for value in entry.values()])

    with open(join(ROOT_JSON, "impianti_gestiti_da_asis.json"), "w+", encoding="utf-8") as f:
        f.write(json.dumps(results_json, indent=4))

    df = pd.DataFrame(data=results_csv, columns=list(results_json[0].keys()))
    df.to_csv(join(ROOT_CSV, "impianti_gestiti_da_asis.csv"), index=False, sep=";")

def impianti_gestiti_da_terzi() -> list:

    results_json = []
    results_csv = []
    
    url = "https://www.comune.trento.it/Aree-tematiche/Sport/Impianti-sportivi/Impianti-gestiti-da-terzi"

    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")

    items = soup.find_all("div", {"class": "class-luogo media"})

    for index1, item in enumerate(items):

        url = item.find("a").attrs["href"]
        url = "https://www.comune.trento.it" + url
        
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")

        name = soup.find("div", {"class": "content-title"}).text.strip()
        name = re.sub(r'\n+', ' ', name)

        print(" "*100, end="\r")
        print(f"[{index1 + 1} / {len(items)}] {name}", end="\r")

        description = soup.find("div", {"class": "media"}).text.strip()
        description = re.sub(r'\n+', '\n', description)

        details = soup.find("div", {"class": "content-detail"}).find_all("div", {"class": "row"})
        details_json = {}

        for detail in details:
            detail_key = detail.find("div", {"class": "col-md-3"})
            detail_key = detail_key.text.strip().lower()

            detail_value = detail.find("div", {"class": "col-md-9"})
            detail_value = detail_value.text.strip().lower()

            key = details_map.get(detail_key)

            if key is None:
                continue

            details_json[key] = detail_value
        
        entry = {
            "name": name,
            "description": description
        }

        entry.update(details_json)

        if entry in results_json:
            continue

        results_json.append(entry)
        results_csv.append([value for value in entry.values()])

    with open(join(ROOT_JSON, "impianti_gestiti_da_terzi.json"), "w+", encoding="utf-8") as f:
        f.write(json.dumps(results_json, indent=4))

    df = pd.DataFrame(data=results_csv, columns=list(results_json[0].keys()))
    df.to_csv(join(ROOT_CSV, "impianti_gestiti_da_terzi.csv"), index=False, sep=";")

impianti_ad_accesso_libero()
impianti_gestiti_da_asis()
impianti_gestiti_da_terzi()
