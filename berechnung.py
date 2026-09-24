"""
Rechenfunktionen für die Bassreflex-Optimierung.
Alle mathematischen Berechnungen für die Kanallänge und Optimierung.
"""

import numpy as np
from scipy.optimize import minimize

from konstanten import f_b, c, k, D_min_cm, OPT_VOLUMEN_MIN, OPT_VOLUMEN_MAX, OPT_DURCHMESSER_MIN, OPT_DURCHMESSER_MAX

def berechne_L_cm(V_liter: float, D_cm: float) -> float:
    """
    Berechnet die Kanallänge L in cm basierend auf Volumen und Durchmesser.

    Args:
        V_liter: Gehäusevolumen in Litern
        D_cm: Kanal-Durchmesser in cm

    Returns:
        float: Kanallänge in cm
    """
    V_m3 = V_liter / 1000.0
    r_m = (D_cm / 100.0) / 2.0
    A_m2 = np.pi * (r_m ** 2)
    L_m = ((c**2) * A_m2) / (4 * (np.pi**2) * (f_b**2) * V_m3) - (k * r_m)

    return L_m * 100.0

def zielfunktion(x: list) -> float:
    """
    Zielfunktion für die Optimierung: Minimiere Volumen.

    Args:
        x: Array [Volumen (Liter), Durchmesser (cm)]

    Returns:
        float: Volumen zum Minimieren
    """
    return x[0]

def constraint_passform(x: list) -> float:
    """
    Constraint-Funktion: Das Rohr muss inklusive Sicherheitsabstand in der Kiste passen.

    Args:
        x: Array [Volumen (Liter), Durchmesser (cm)]

    Returns:
        float: Constraint-Wert (>= 0 für erfüllt)
    """
    V_liter, D_cm = x
    kantenlaenge_cm = (V_liter / 1000.0)**(1/3) * 100.0
    L_cm = berechne_L_cm(V_liter, D_cm)
    return (kantenlaenge_cm - D_cm) - L_cm

def berechne_optimum() -> tuple:
    """
    Berechnet das mathematische Optimum für Volumen und Durchmesser.

    Returns:
        tuple: (optimales_Volumen, optimaler_Durchmesser, optimale_Kanallänge)
    """
    bounds = [
        (OPT_VOLUMEN_MIN, OPT_VOLUMEN_MAX),
        (OPT_DURCHMESSER_MIN, OPT_DURCHMESSER_MAX)
    ]
    constraints = [{'type': 'ineq', 'fun': constraint_passform}]

    ergebnis = minimize(
        zielfunktion,
        [15.0, 6.0],
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    opt_V = ergebnis.x[0]
    opt_D = ergebnis.x[1]
    opt_L = berechne_L_cm(opt_V, opt_D)

    return opt_V, opt_D, opt_L

def berechne_grid(volumen_liter: np.ndarray, durchmesser_cm: np.ndarray) -> tuple:
    """
    Berechnet ein 3D-Grid für die Visualisierung.

    Args:
        volumen_liter: Array von Volumenwerten in Litern
        durchmesser_cm: Array von Durchmesserwerten in cm

    Returns:
        tuple: (V_grid, D_grid, L_grid) - Meshgrid und Kanallängen
    """
    V_grid, D_grid = np.meshgrid(volumen_liter, durchmesser_cm)
    L_grid = berechne_L_cm(V_grid, D_grid)
    L_grid[L_grid < 0] = np.nan  # Physikalisch unmögliche Werte ausblenden

    return V_grid, D_grid, L_grid