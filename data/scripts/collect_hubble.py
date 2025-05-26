# scripts/collect_hubble.py

import requests
import csv
from datetime import datetime

# Exemple : API simulée H(z) - remplacer par une API réelle ou fichier brut si nécessaire
url = "https://api.mocki.io/v2/549a5d8b/HubbleData"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    # Crée un fichier CSV
    filename = f"hubble_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["redshift_z", "Hubble_Hz", "uncertainty"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in data["values"]:
            writer.writerow({
                "redshift_z": item["z"],
                "Hubble_Hz": item["H"],
                "uncertainty": item.get("uncertainty", "N/A")
            })

    print(f"Données sauvegardées dans : {filename}")

else:
    print("Erreur lors de la récupération des données :", response.status_code)
