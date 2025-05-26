# scripts/collect_hubble.py

import requests
import csv
from datetime import datetime

# Coordonnées de la région d'intérêt (ex : Andromède)
ra = 10.684  # Ascension droite (RA) en degrés
dec = 41.269  # Déclinaison (Dec) en degrés
radius = 0.1  # Rayon en degrés

# URL API MAST - Hubble Source Catalog
url = f"https://mast.stsci.edu/api/v0.1/hsc/search?ra={ra}&dec={dec}&radius={radius}"

# Requête GET
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    filename = f"../data/cosmologie/hubble_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Champs disponibles dans la réponse
    fieldnames = data.get("fields", [])

    if not fieldnames:
        print("Pas de données reçues.")
    else:
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data.get("data", []):
                writer.writerow(row)

        print(f"Données sauvegardées dans : {filename}")

else:
    print("Erreur lors de la récupération des données :", response.status_code)
