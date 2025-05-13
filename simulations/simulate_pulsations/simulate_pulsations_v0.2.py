import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
import os  # Ajouté pour résoudre le problème de chemin

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "../../data/social/france_hashtags_2024.csv")
    df = pd.read_csv(data_path)
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

# Préparer les données des mentions pour η(t) et la visualisation
df['date'] = pd.to_datetime(df['date'])
df['years_since_2024'] = (df['date'] - pd.to_datetime("2024-01-01")).dt.total_seconds() / (365.25 * 24 * 60 * 60)
retraites = df[df['hashtag'] == "#retraites"]
carburant = df[df['hashtag'] == "#carburant"]

# Interpolation des mentions sur la période 2025-2030
mentions_max = 10000
if len(retraites) > 1:
    interp_retraites = interp1d(retraites['years_since_2024'], retraites['mentions'], kind='linear', fill_value="extrapolate")
    mentions_retraites = interp_retraites(t + 1)
else:
    mentions_retraites = retraites['mentions'].iloc[0] * np.ones(len(t))

if len(carburant) > 1:
    interp_carburant = interp1d(carburant['years_since_2024'], carburant['mentions'], kind='linear', fill_value="extrapolate")
    mentions_carburant = interp_carburant(t + 1)
else:
    mentions_carburant = carburant['mentions'].iloc[0] * np.ones(len(t))

eta_t = eta_0 * (1 + chi * X_t) * (1 + (mentions_retraites + mentions_carburant) / (2 * mentions_max))

delta_fractal = np.zeros(len(t))
for n in range(1, 100):
    omega_n = omega_human / n + omega_cosmic
    delta_fractal += alpha * np.sin(omega_n * t * 365.25 * 24 * 3600) / (n**2)

theta_n = np.zeros(len(t))
dtheta_n = np.zeros(len(t))
theta_n[0] = 0.019
dtheta_n[0] = 0.0
for i in range(1, len(t)):
    d2_theta = -kappa * theta_n[i-1] - gamma * dtheta_n[i-1] + eta_t[i-1] * delta_fractal[i-1]
    dtheta_n[i] = dtheta_n[i-1] + d2_theta * dt
    theta_n[i] = theta_n[i-1] + dtheta_n[i] * dt

T_t = beta * theta_n

np.savetxt("theta_n.txt", theta_n)
np.savetxt("T_t.txt", T_t)

plt.figure(figsize=(10, 6))
plt.plot(t + 2025, theta_n, label="θ_n(t) (Pulsations Humaines)", color="blue")
plt.plot(t + 2025, T_t, label="T(t) (Lutte de Classes)", color="red")
plt.plot(t + 2025, mentions_retraites / mentions_max * 0.03, label="Mentions #retraites (normalisées)", linestyle="--", color="green")
plt.plot(t + 2025, mentions_carburant / mentions_max * 0.03, label="Mentions #carburant (normalisées)", linestyle="--", color="orange")
plt.xlabel("Année")
plt.ylabel("Amplitude")
plt.title("Pulsations Fractales 2025–2030 avec Données Sociales")
plt.legend()
plt.grid(True)
plt.savefig("pulsations_2025_2030_with_data.png")
plt.show()
