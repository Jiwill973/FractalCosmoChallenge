import numpy as np
import matplotlib.pyplot as plt

# Paramètres
kappa = 1e-3  # Constante de rappel
eta_0 = 0.005  # Couplage initial
chi = 0.5  # Influence de X(t)
alpha = 0.01  # Amplitude des fluctuations fractales
omega_n = 1e-18  # Fréquence cosmique
beta = 0.1  # Couplage T(t) et θ_n(t)
X_t = 1.5  # Amplification par X (2025)
t = np.linspace(0, 5, 1000)  # Temps (2025–2030, 5 ans)

# Fluctuations fractales
delta_fractal = np.zeros(len(t))
for n in range(1, 100):
    delta_fractal += alpha * np.sin(omega_n * t) / (n**2)

# Calcul de θ_n(t)
theta_n = np.zeros(len(t))
eta_t = eta_0 * (1 + chi * X_t)  # Couplage ajusté
dt = t[1] - t[0]
theta_n[0] = 0.019  # Condition initiale (ex. Haïti 1791)
for i in range(1, len(t)):
    d2_theta = -kappa * theta_n[i-1] + eta_t * delta_fractal[i-1]
    theta_n[i] = theta_n[i-1] + d2_theta * dt**2

# Calcul de T(t)
T_t = beta * theta_n

# Visualisation
plt.plot(t + 2025, theta_n, label="θ_n(t) (Pulsations Humaines)")
plt.plot(t + 2025, T_t, label="T(t) (Lutte de Classes)")
plt.xlabel("Année")
plt.ylabel("Amplitude")
plt.title("Pulsations Fractales 2025–2030")
plt.legend()
plt.savefig("pulsations_2025_2030.png")
plt.show()
