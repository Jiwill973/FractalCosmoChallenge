import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d

# Paramètres ajustés
kappa = 0.1
eta_0 = 0.1
chi = 1.0
alpha = 0.1
beta = 0.2
X_t = 2.0
gamma = 0.01
t = np.linspace(0, 5, 1000)
dt = t[1] - t[0]

f_human = 1 / (365.25 * 24 * 3600)
omega_human = 2 * np.pi * f_human
omega_cosmic = 1e-18

# Charger les données sociales (ex. hashtags)
try:
    df = pd.read_csv("data/social/france_hashtags_2024.csv")
    print("Données chargées avec succès :")
    print(df.head())
    print("Colonnes disponibles :", df.columns.tolist())
    print("Nombre de lignes :", len(df))
except Exception as e:
    print("Erreur lors du chargement des données :", str(e))
    print("Données non trouvées, utilisation de mentions simulées.")
    # Simuler des données si nécessaire
    dates = pd.date_range(start="2024-01-01", end="2024-01-04", freq="D")
    df = pd.DataFrame({
        "date": dates,
        "hashtag": ["#retraites", "#retraites", "#carburant", "#carburant"],
        "mentions": [5000, 5200, 3000, 3100]
    })
