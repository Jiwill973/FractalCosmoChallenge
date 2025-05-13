import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d

# Paramètres
kappa = 1e-3  # Constante de rappel (1/s^2)
eta_0 = 0.005  # Couplage initial
chi = 0.5  # Influence de X(t)
alpha = 0.01  # Amplitude des fluctuations fractales
beta = 0.1  # Couplage T(t) et θ_n(t)
X_t = 1.5  # Amplification par X (2025)
gamma = 0.1  # Coefficient d’amortissement (1/s)
mentions_max = 10000  # Valeur maximale des mentions pour normalisation

# Définir le temps en années et en secondes
t_years = np.linspace(0, 5, 1000)  # 0 à 5 ans (2025-2030)
seconds_per_year = 365.25 * 24 * 3600
t_seconds = t_years * seconds_per_year
dt = t_seconds[1] - t_seconds[0]  # Pas de temps en secondes

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
    dates = pd.date_range(start="2024-01-01", end="2024-01-04", freq="D")
    df = pd.DataFrame({
        "date": dates,
        "hashtag": ["#retraites", "#retraites", "#carburant", "#carburant"],
        "mentions": [5000, 5200, 3000, 3100]
    })

# Préparer les données des mentions
df['date'] = pd.to_datetime(df['date'])
df['years_since_2024'] = (df['date'] - pd.to_datetime("2024-01-01")).dt.total_seconds() / (365.25 * 24 * 60 * 60)
retraites = df[df['hashtag'] == "#retraites"]
carburant = df[df['hashtag'] == "#carburant"]

# Interpolation des mentions sur la période 2025-2030
if len(retraites) > 1:
    interp_retraites = interp1d(retraites['years_since_2024'], retraites['mentions'], kind='linear', fill_value="extrapolate")
    mentions_retraites = interp_retraites(t_years + 1)  # t + 1 car 2025 est 1 an après 2024
else:
    mentions_retraites = retraites['mentions'].iloc[0] * np.ones(len(t_years))
if len(carburant) > 1:
    interp_carburant = interp1d(carburant['years_since_2024'], carburant['mentions'], kind='linear', fill_value="extrapolate")
    mentions_carburant = interp_carburant(t_years + 1)
else:
    mentions_carburant = carburant['mentions'].iloc[0] * np.ones(len(t_years))

# Calcul de eta_t dynamique
eta_t = eta_0 * (1 + chi * X_t) * (1 + (mentions_retraites + mentions_carburant) / mentions_max)

# Fluctuations fractales avec spectre P(f) ∝ f^{-2}
N = 100
f_min = 1.59e-19  # Hz (correspond à ω ≈ 10^{-18} rad/s)
f_max = 1e-7  # Hz (échelles humaines)
f_n = f_min * (f_max / f_min)**(np.arange(N) / (N - 1))
omega_n = 2 * np.pi * f_n
a_n = alpha / f_n
delta_fractal = np.zeros_like(t_seconds)
for n in range(N):
    delta_fractal += a_n[n] * np.sin(omega_n[n] * t_seconds)

# Calcul de θ_n(t) avec amortissement
theta_n = np.zeros(len(t_seconds))
v_n = npotropinés", linestyle="--", color="green")
plt.plot(t_years + 2025, mentions_carburant / mentions_max * 0.03, label="Mentions #carburant (normalisées)", linestyle="--", color="orange")
plt.xlabel("Année")
plt.ylabel("Amplitude")
plt.title("Pulsations Fractales 2025–2030 avec Données Sociales")
plt.legend()
plt.grid(True)
plt.savefig("pulsations_2025_2030_with_data.png")
plt.show()
