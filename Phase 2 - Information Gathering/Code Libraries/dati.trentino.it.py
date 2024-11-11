import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import json
from os.path import isfile, join, dirname, exists
from os import makedirs, chdir
import io
import pandas as pd
import shutil

chdir(dirname(__file__))

ROOT: str = "../data/raw/dati.trentino.it"
ROOT_JSON = join(ROOT, "json")
ROOT_CSV = join(ROOT, "csv")

if exists(ROOT):
    shutil.rmtree(ROOT)

makedirs(ROOT, exist_ok=True)
makedirs(ROOT_JSON, exist_ok=True)
makedirs(ROOT_CSV, exist_ok=True)

def is_valid_csv(csv_string: str) -> bool:

    try:
        csv_file = io.StringIO(csv_string)
    except:
        return False
    
    try:

        pd.read_csv(csv_file, sep=";")
        return True

    except:
        pass

    try:

        pd.read_csv(csv_file, sep=",")
        return True

    except:
        pass

    return False

page = 1

current_result = 0
total_results = None

while True:
    url = f"https://dati.trentino.it/dataset?q=eventi&page={page}"

    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")

    if total_results is None:
        total_results = soup.find("form", {"id": "dataset-search-form"})
        total_results = total_results.find("h2").text
        total_results = int(re.findall(r'\d+', total_results)[0])
    
    items = soup.find_all("li", {"class": "dataset-item"})

    if not len(items):
        break

    page = page + 1

    for item in items:

        url = item.find("a").attrs["href"]
        url = f"https://dati.trentino.it{url}"

        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")

        name = soup.find("section", {"class": "module-content"}).find("h1").text
        name = re.sub(r'\n+', '\n', name).strip()
        name = re.sub(r'[^\x00-\x7F]+', '', name)
        name = name.replace("Comune di", "").strip()
        
        current_result = current_result + 1

        print(" "*100, end="\r")
        print(f"[{current_result} / {total_results}] {name}", end="\r")

        resources = soup.find_all("li", {"class": "resource-item"})

        csv_resource = [resource.find_all("li")[1].find("a").attrs["href"] for resource in resources if resource.find("span", {"data-format": "csv"})]

        if len(csv_resource):

            if isfile(join(ROOT_CSV, f"{name}.csv")):
                continue

            response = requests.get(url=csv_resource[0])

            if not is_valid_csv(csv_string=response.text):
                continue

            with open(join(ROOT_CSV, f"{name}.csv"), "w+", encoding="utf-8") as f:
                f.write(response.text)

            continue
        
        if isfile(join(ROOT_JSON, f"{name}.json")):
            continue

        json_resource = [resource.find_all("li")[1].find("a").attrs["href"] for resource in resources if resource.find("span", {"data-format": "json"})][0]

        current_events = []
        final_results_csv = []

        while json_resource is not None:

            response = requests.get(url=json_resource)

            try:
                data = response.json()
            except:

                if response.status_code == 429:
                    sleep(5)
                    continue

                print(json_resource)
                break
            
            if isinstance(data, list):
                current_events.extend(data)
                final_results_csv.extend([list(event.values()) for event in data])
                break

            else:

                items = data["searchHits"]

                current_events.extend(items)
                final_results_csv.extend([list(event["data"]["ita-IT"].values()) for event in items])

                json_resource = data["nextPageQuery"]

        if len(current_events):
            with open(join(ROOT_JSON, f"{name}.json"), "w+", encoding="utf-8") as f:
                f.write(json.dumps(current_events, indent=4))

            df = pd.DataFrame(data=final_results_csv, columns=list(current_events[0].keys()))
            df.to_csv(join(ROOT_CSV, f"{name}.csv"), index=False, sep=";")

