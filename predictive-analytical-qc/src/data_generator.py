import numpy as np
import pandas as pd

def generate_qc_series(n_days=30, target=1.00, cv_pct=2.0, drift_start_day=10, seed=42):
    """
    Génère une série temporelle de contrôle qualité simulant une dérive physique progressive.
    
    Paramètres:
    - n_days : Nombre total de jours d'analyse (défaut : 30).
    - target : Valeur cible nominale en g/L (défaut : 1.00).
    - cv_pct : Coefficient de variation nominal en % (défaut : 2.0%).
    - drift_start_day : Jour de début de la dégradation instrumentale (défaut : 10).
    - seed : Graine aléatoire pour la reproductibilité.
    """
    np.random.seed(seed)
    days = np.arange(1, n_days + 1)
    sigma_nominal = target * (cv_pct / 100.0)
    
    # Biais systématique (dérive progressive de pente / vieillissement réactif)
    bias = np.zeros(n_days)
    if drift_start_day < n_days:
        drift_len = n_days - drift_start_day + 1
        bias[drift_start_day - 1:] = np.linspace(0.0, 0.045, drift_len)  # Dérive jusqu'à +4.5%
        
    # Dispersion analytique croissante (perte de fidélité)
    dispersion = np.ones(n_days) * sigma_nominal
    if drift_start_day < n_days:
        dispersion[drift_start_day - 1:] = np.linspace(sigma_nominal, sigma_nominal * 1.8, drift_len)
        
    # Mesures simulées avec bruit gaussien
    measured_values = target + bias + np.random.normal(0, dispersion)
    
    df = pd.DataFrame({
        "day": days,
        "target": target,
        "measured": measured_values
    })
    return df

if __name__ == "__main__":
    df_qc = generate_qc_series()
    df_qc.to_csv("../data/qc_measurements.csv", index=False)
    print("Données QC synthétiques générées avec succès dans data/qc_measurements.csv")