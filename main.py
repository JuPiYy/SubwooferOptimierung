import numpy as np
import matplotlib.pyplot as plt

# Importiere Konstanten und Rechenfunktionen aus separaten Modulen
from konstanten import f_b, VOLUMEN_MIN, VOLUMEN_MAX, VOLUMEN_SCHRITTE, DURCHMESSER_MIN, DURCHMESSER_MAX, DURCHMESSER_SCHRITTE
from berechnung import berechne_L_cm, berechne_optimum, berechne_grid

# --- 1. Mathematisches Optimum berechnen ---
opt_V, opt_D, opt_L = berechne_optimum()

# --- 2. 3D-Grid für die Oberfläche erstellen ---
volumen_liter = np.linspace(VOLUMEN_MIN, VOLUMEN_MAX, VOLUMEN_SCHRITTE)
durchmesser_cm = np.linspace(DURCHMESSER_MIN, DURCHMESSER_MAX, DURCHMESSER_SCHRITTE)
V_grid, D_grid, L_grid = berechne_grid(volumen_liter, durchmesser_cm)

# --- 4. Visualisierung mit Matplotlib ---
fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection='3d')

# 3D-Oberfläche plotten
surf = ax.plot_surface(V_grid, D_grid, L_grid, cmap='viridis', alpha=0.7, edgecolor='none')

# Optimalen Punkt im 3D-Raum einzeichnen (roter Punkt)
ax.scatter([opt_V], [opt_D], [opt_L], color='red', s=100, zorder=5, label='Mathematisches Optimum')

# Hilfslinien vom Optimum zu den Achsen zeichnen
ax.plot([opt_V, opt_V], [opt_D, opt_D], [0, opt_L], color='red', linestyle='--', linewidth=1.5)

# Text-Beschriftung am Optimum
ax.text(opt_V + 1, opt_D, opt_L + 2, 
        f" Optimum:\n V = {opt_V:.2f} L\n D = {opt_D:.2f} cm\n L = {opt_L:.2f} cm", 
        color='black', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))

# Achsenbeschriftungen & Titel
ax.set_xlabel('Gehäusevolumen (Liter)')
ax.set_ylabel('Kanal-Durchmesser (cm)')
ax.set_zlabel('Kanallänge (cm)')
ax.set_title(f'Bassreflex-Optimierung ($f_b = {f_b:.0f}$ Hz)', fontsize=12, fontweight='bold')

fig.colorbar(surf, shrink=0.5, aspect=8, label='Kanallänge (cm)')
ax.legend(loc='upper left')

plt.show()