"""
Konstanten und Konfigurationswerte für die Bassreflex-Optimierung.
"""

# Physikalische Konstanten
f_b = 40.0              # Ziel-Abstimmfrequenz in Hz
c = 343.0               # Schallgeschwindigkeit in m/s
k = 0.825               # Mündungskorrektur

# Geometrische Grenzen
D_min_cm = 5.0          # Mindestdurchmesser gegen Strömungsgeräusche (cm)

# Grid-Parameter für 3D-Visualisierung
VOLUMEN_MIN = 5         # Minimum Gehäusevolumen in Litern
VOLUMEN_MAX = 30        # Maximum Gehäusevolumen in Litern
VOLUMEN_SCHRITTE = 50   # Anzahl der Schritte für das Volumen-Grid

DURCHMESSER_MIN = 3     # Minimum Kanal-Durchmesser in cm
DURCHMESSER_MAX = 10    # Maximum Kanal-Durchmesser in cm
DURCHMESSER_SCHRITTE = 50  # Anzahl der Schritte für das Durchmesser-Grid

# Optimierungsgrenzen
OPT_VOLUMEN_MIN = 5.0   # Minimum für Optimierung in Litern
OPT_VOLUMEN_MAX = 30.0  # Maximum für Optimierung in Litern
OPT_DURCHMESSER_MIN = D_min_cm  # Minimum für Optimierung in cm
OPT_DURCHMESSER_MAX = 10.0      # Maximum für Optimierung in cm
