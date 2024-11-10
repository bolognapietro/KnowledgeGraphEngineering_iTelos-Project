import requests
import re
from os.path import isfile, join, dirname
from os import makedirs, chdir
import shutil
import json
import pandas as pd

chdir(dirname(__file__))

ROOT: str = "../data/raw/paginegialle.it"
ROOT_JSON = join(ROOT, "json")
ROOT_CSV = join(ROOT, "csv")

shutil.rmtree(ROOT)

makedirs(ROOT, exist_ok=True)
makedirs(ROOT_JSON, exist_ok=True)
makedirs(ROOT_CSV, exist_ok=True)

municipalities = [
    'Ala', 'Albiano', 'Aldeno', 'Altavalle', 'Altopiano della Vigolana', 'Amblar-Don', 'Andalo', 'Arco', 'Avio', 
    'Baselga di Pinè', 'Bedollo', 'Besenello', 'Bieno', 'Bleggio Superiore', 'Bocenago', 'Bondone', 'Borgo Chiese', 
    'Borgo Lares', 'Borgo Valsugana', 'Brentonico', 'Bresimo', 'Brez', 'Caderzone Terme', 'Cagno\' Novella', 'Calceranica al Lago', 
    'Caldes', 'Caldonazzo', 'Calliano', 'Campitello di Fassa', 'Campodenno', 'Canal San Bovo', 'Canazei', 'Capriana', 
    'Ville di Fiemme', 'Carisolo', 'Carzano', 'Castel Condino', 'Castel Ivano', 'Castelfondo', 'Castello-Molina di Fiemme', 
    'Castello Tesino', 'Castelnuovo', 'Cavalese', 'Cavareno', 'Cavedago', 'Cavedine', 'Cavizzana', 'Cembra Lisignago', 
    'Cimone', 'Cinte Tesino', 'Cis', 'Civezzano', 'Cles', 'Cloz', 'Comano Terme', 'Commezzadura', 'Contà', 'Croviana', 
    'Daiano', 'Dambel', 'Denno', 'Dimaro Folgarida', 'Drena', 'Dro', 'Faedo San Michele all\'Adige', 'Fai della Paganella', 'Fiavè', 'Fierozzo', 
    'Folgaria', 'Fondo Borgo d\'Anaunia', 'Fornace', 'Frassilongo', 'Garniga Terme', 'Giovo', 'Giustino', 'Grigno', 'Imer', 'Isera', 
    'Lavarone', 'Lavis', 'Ledro', 'Levico Terme', 'Livo', 'Lona-Lases', 'Luserna', 'Madruzzo', 'Malè', 'Malosco', 
    'Massimeno', 'Mazzin', 'Mezzana', 'Mezzano', 'Mezzocorona', 'Mezzolombardo', 'Moena', 'Molveno', 'Mori', 
    'Nago-Torbole', 'Nave San Rocco', 'Nogaredo', 'Nomi', 'Novaledo', 'Ospedaletto', 'Ossana', 'Palù del Fersina', 
    'Panchià', 'Peio', 'Pellizzano', 'Pelugo', 'Pergine Valsugana', 'Pieve di Bono-Prezzo', 'Pieve Tesino', 'Pinzolo', 
    'Pomarolo', 'Porte di Rendena', 'Predaia', 'Predazzo', 'Primiero San Martino di Castrozza', 'Rabbi', 'Revò', 
    'Riva del Garda', 'Romallo', 'Romeno', 'Roncegno Terme', 'Ronchi Valsugana', 'Ronzo-Chienis', 'Ronzone', 
    'Roverè della Luna', 'Rovereto', 'Ruffrè-Mendola', 'Rumo', 'Sagron Mis', 'Samone', 'San Lorenzo Dorsino', 
    "San Michele all'Adige", "Sant'Orsola Terme", 'Sanzeno', 'Sarnonico', 'Scurelle', 'Segonzano', 'Sella Giudicarie', 
    'San Giovanni di Fassa', 'Sfruz', 'Soraga di Fassa', 'Sover', 'Spiazzo', 'Spormaggiore', 'Sporminore', 'Stenico', 
    'Storo', 'Strembo', 'Telve', 'Telve di Sopra', 'Tenna', 'Tenno', 'Terragnolo', 'Terzolas', 'Tesero', 'Tione di Trento', 
    'Ton', 'Torcegno', 'Trambileno', 'Tre Ville', 'Trento', 'Valdaone', 'Valfloriana', 'Vallarsa', 'Vallelaghi', 'Varena', 
    'Vermiglio', 'Vignola-Falesina', 'Villa Lagarina', "Ville d'Anaunia", 'Volano', 'Zambana', 'Ziano di Fiemme'
]

for index1, municipality in enumerate(municipalities):

    print(" "*100, end="\r")
    print(f"[{index1+1} / {len(municipalities)}] {municipality}", end="\r")

    if isfile(join(ROOT_JSON, f"{municipality}.json")) and isfile(join(ROOT_CSV, f"{municipality}.csv")):
        continue

    final_results_json = []
    final_results_csv = []

    page = 1

    municipality_paginegialle = municipality

    while True:

        url = f"https://www.paginegialle.it/ricerca/impianto%20sportivo/{municipality_paginegialle}/p-{page}?output=json"

        response = requests.get(url=url)

        if response.status_code == 404:

            if len(final_results_json):
                with open(join(ROOT_JSON, f"{municipality}.json"), "w+") as f:
                    f.write(json.dumps(final_results_json, indent=4))
                
                df = pd.DataFrame(data=final_results_csv, columns=list(final_results_json[0].keys()))
                df.to_csv(join(ROOT_CSV, f"{municipality}.csv"), index=False, sep=";")

            break
    
        data = response.json()

        error = data.get("error", {})

        if len(error):
            
            suggestions = data.get("list", {}).get("suggest", {}).get("multiloc", [])
            best_suggestion = [suggestion for suggestion in suggestions if "trentino alto adige" in suggestion["reg"].lower()]

            if len(best_suggestion):
                municipality_paginegialle = best_suggestion[0].get("fraz")

                if municipality_paginegialle is None:
                    municipality_paginegialle = f"{municipality} ({best_suggestion[0]['cd_prv']})"
                else:
                    municipality_paginegialle = best_suggestion[0]["com"] + " " + municipality_paginegialle

                continue

            if len(final_results_json):
                with open(join(ROOT_JSON, f"{municipality}.json"), "w+") as f:
                    f.write(json.dumps(final_results_json, indent=4))
                
                df = pd.DataFrame(data=final_results_csv, columns=list(final_results_json[0].keys()))
                df.to_csv(join(ROOT_CSV, f"{municipality}.csv"), index=False, sep=";")

            break

        results = data.get("list", {}).get("out", {}).get("base", {}).get("results", [])
        
        for index2, result in enumerate(results):

            print(" "*100, end="\r")
            print(f"[{index1+1} / {len(municipalities)}] {municipality} {len(final_results_json) + index2}", end="\r")

            result_name = result.get("ds_insegna", "")

            if not len(result_name):
                result_name = result.get("ds_ragsoc", "")

            result_name = re.sub(r'[^\x00-\x7F]+', '', result_name.strip())

            result_comune = result.get("ds_comune_ita")
            result_comune = re.sub(r'[^\x00-\x7F]+', '', result_comune.strip())

            result_address = result.get("addr")
            result_address = re.sub(r'[^\x00-\x7F]+', '', result_address.strip())

            result_time = result.get("time", {})
            result_time_formatted = {}

            for day, times in result_time.items():

                day = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][int(day) - 1]
                times = " / ".join(times)

                result_time_formatted[day] = times
            
            result_phones = [re.sub(r'\D', '', phone) for phone in result.get("ds_ls_telefoni", [])]
            result_phones.extend([re.sub(r'\D', '', phone) for phone in result.get("ds_ls_telefoni_whatsapp", [])])
            result_phones = list(set(result_phones))

            result_website = result.get("site_link", {}).get("url")
            
            final_results_json.append({
                "name": result_name,
                "address": result_address,
                "comune": result_comune,
                "open_hours": result_time_formatted,
                "phone_number": result_phones,
                "website": result_website
            })

            final_results_csv.append([
                result_name,
                result_address,
                result_comune,
                '"' + ', '.join([f'{key}: {value}' for key, value in result_time_formatted.items()]) + '"',
                " ".join(result_phones),
                result_website
            ])

        page = page + 1