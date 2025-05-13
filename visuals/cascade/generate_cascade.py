import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Charger les données simulées (ou réelles)
t = np.linspace(0, 5, 1000) + 2025  # Années 2025–2030
theta_n = np.loadtxt("../../simulations/simulate_pulsations/simulate_pulsations_results_v0.2/theta_n.txt")  # Supposons que θ_n(t) est sauvegardé
T_t = np.loadtxt("../../simulations/simulate_pulsations/simulate_pulsations_results_v0.2/T_t.txt")  # Supposons que T(t) est sauvegardé
try:
    data = pd.read_csv("../../data/social/france_hashtags_2024.csv")
    mentions = data[data["hashtag"] == "#retraites"]["mentions"].values
    mentions = np.interp(np.linspace(0, 5, 1000), np.linspace(0, 5, len(mentions)), mentions)
    mentions_max = mentions.max() or 1
except FileNotFoundError:
    mentions = np.ones(len(t)) * 5000
    mentions_max = 5000

# Créer le graphique interactif
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Pulsations Fractales", "Données Sociales"))
fig.add_trace(go.Scatter(x=t, y=theta_n, name="θ_n(t) (Pulsations Humaines)", line=dict(color="blue")), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=T_t, name="T(t) (Lutte de Classes)", line=dict(color="red")), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=mentions / mentions_max * 0.03, name="Mentions #retraites (normalisées)", line=dict(color="green", dash="dash")), row=2, col=1)
fig.update_layout(title="Cascade Fractale 2025–2030", xaxis_title="Année", yaxis_title="Amplitude")
fig.write_html("cascade_2025_2030.html")
