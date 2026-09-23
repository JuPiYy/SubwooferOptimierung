import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# --- 1. Parameter definieren ---
f_b = 40.0          # Ziel-Abstimmfrequenz in Hz
c = 343.0           # Schallgeschwindigkeit in m/s
k = 0.825           # Mündungskorrektur
D_min_cm = 5.0      # Mindestdurchmesser gegen Strömungsgeräusche (cm)

# Funktion zur Berechnung der Kanallänge L (in cm)
def berechne_L_cm(V_liter, D_cm):
    V_m3 = V_liter / 1000.0
    r_m = (D_cm / 100.0) / 2.0
    A_m2 = np.pi * (r_m ** 2)
    L_m = ((c**2) * A_m2) / (4 * (np.pi**2) * (f_b**2) * V_m3) - (k * r_m)
    return L_m * 100.0

# --- 2. Mathematisches Optimum berechnen ---
def zielfunktion(x):
    return x[0]  # Volumen V minimieren

def constraint_passform(x):
    V_liter, D_cm = x
    kantenlaenge_cm = (V_liter / 1000.0)**(1/3) * 100.0
    L_cm = berechne_L_cm(V_liter, D_cm)
    # Rohr muss inklusive Sicherheitsabstand in Kiste passen
    return (kantenlaenge_cm - D_cm) - L_cm

bounds = [(5.0, 30.0), (D_min_cm, 10.0)]  # Grenzen für V (Liter) und D (cm)
constraints = [{'type': 'ineq', 'fun': constraint_passform}]

ergebnis = minimize(zielfunktion, [15.0, 6.0], method='SLSQP', bounds=bounds, constraints=constraints)

opt_V = ergebnis.x[0]
opt_D = ergebnis.x[1]
opt_L = berechne_L_cm(opt_V, opt_D)

# --- 3. 3D-Grid für die Oberfläche erstellen ---
volumen_liter = np.linspace(5, 30, 50)
durchmesser_cm = np.linspace(3, 10, 50)
V_grid, D_grid = np.meshgrid(volumen_liter, durchmesser_cm)

L_grid = berechne_L_cm(V_grid, D_grid)
L_grid[L_grid < 0] = np.nan  # Physikalisch unmögliche Werte ausblenden

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