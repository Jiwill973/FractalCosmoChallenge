import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Paramètres
kappa = 1e-3  # Constante de rappel
eta_0 = 0.005  # Couplage initial
chi = 0.5  # Influence de X(t)
alpha = 0.01  # Amplitude des fluctuations fractales
omega_n = 1e-18  # Fréquence cosmique
beta = 0.1  # Couplage T(t) et θ_n(t)
X_t = 1.5  # Amplification par X (2025)
t = np.linspace(0, 5, 1000)  # Temps (2025–2030, 5 ans)

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

# Fluctuations fractales
delta_fractal = np.zeros(len(t))
for n in range(1, 100):
    delta_fractal += alpha * np.sin(omega_n * t) / (n**2)

# Calcul de θ_n(t) avec η(t) ajusté dynamiquement
theta_n = np.zeros(len(t))
mentions = df['mentions'].mean()  # Utilise la moyenne des mentions
mentions_max = 10000  # Valeur maximale des mentions pour normalisation
eta_t = eta_0 * (1 + chi * X_t) * (1 + mentions / mentions_max)  # Ajustement par mentions (scalaire)
dt = t[1] - t[0]
theta_n[0] = 0.019  # Condition initiale (ex. Haïti 1791)
for i in range(1, len(t)):
    d2_theta = -kappa * theta_n[i-1] + eta_t * delta_fractal[i-1]  # eta_t est un scalaire, pas besoin de [i]
    theta_n[i] = theta_n[i-1] + d2_theta * dt**2

# Calcul de T(t)
T_t = beta * theta_n

# Sauvegarde des données
np.savetxt("theta_n.txt", theta_n)
np.savetxt("T_t.txt", T_t)

# Visualisation
plt.plot(t + 2025, theta_n, label="θ_n(t) (Pulsations Humaines)")
plt.plot(t + 2025, T_t, label="T(t) (Lutte de Classes)")
plt.plot(t + 2025, mentions / mentions_max * 0.03 * np.ones(len(t)), label="Mentions #retraites
