import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from metrics import calculate_bias_pct, calculate_cv_pct, calculate_total_error, calculate_sigma_metric
from predictor import predict_drift_and_rul
from calibrator import fit_calibration_curve, diagnose_calibration_drift

def run_analytical_pipeline():
    # 1. Chargement des données
    data_path = os.path.join(os.path.dirname(__file__), "../data/qc_measurements.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError("Exécutez d'abord data_generator.py pour créer les données.")
        
    df = pd.read_csv(data_path)
    days = df["day"].values
    measured = df["measured"].values
    target = df["target"].iloc[0]
    
    tea = 6.0  # Erreur Totale Admissible (6.0%)
    fenetre = 6
    n_days = len(days)
    
    total_errors = np.full(n_days, np.nan)
    sigma_scores = np.full(n_days, np.nan)
    
    # 2. Calcul métrologique glissant
    for i in range(fenetre - 1, n_days):
        sub_sample = measured[i - fenetre + 1 : i + 1]
        mean_val = np.mean(sub_sample)
        std_val = np.std(sub_sample, ddof=1)
        
        b_pct = calculate_bias_pct(mean_val, target)
        c_pct = calculate_cv_pct(std_val, mean_val)
        
        total_errors[i] = calculate_total_error(b_pct, c_pct)
        sigma_scores[i] = calculate_sigma_metric(tea, b_pct, c_pct)
        
    # 3. Prédiction au Jour 18
    day_diag = 18
    w_start = day_diag - fenetre
    pente, ordonnee, rul, jour_rupture = predict_drift_and_rul(
        days[w_start:day_diag],
        total_errors[w_start:day_diag],
        threshold=tea,
        current_day=day_diag
    )
    
    # 4. Diagnostic d'étalonnage
    std_conc = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    abs_j1 = 0.450 * std_conc + 0.010
    slope_init, int_init, _ = fit_calibration_curve(std_conc, abs_j1)
    
    abs_diag = (0.450 * 0.82) * std_conc + 0.022  # Dégradation simulée
    slope_curr, int_curr, _ = fit_calibration_curve(std_conc, abs_diag)
    
    diag_res = diagnose_calibration_drift(slope_init, slope_curr, int_init, int_curr)
    
    # 5. Affichage du bilan
    print("==================================================")
    print(" RAPPORT MÉTROLOGIQUE ET PRÉDICTION ANALYTIQUE")
    print("==================================================")
    print(f"Jour du diagnostic           : J{day_diag}")
    print(f"Erreur Totale mesurée         : {total_errors[day_diag-1]:.2f}% (Seuil TEa: {tea}%)")
    print(f"Indice Six Sigma              : {sigma_scores[day_diag-1]:.2f} σ")
    print(f"Vitesse d'altération          : +{pente:.3f}% TE/jour")
    print(f"RUL (Temps avant non-conformité): {rul:.1f} jours")
    print(f"Diagnostic d'étalonnage       : {diag_res['diagnosis']}")
    print(f"Décision automatisée          : {'[RÉÉTALONNAGE REQUIS]' if diag_res['needs_recalibration'] else '[CONFORME]'}")
    print("==================================================")

if __name__ == "__main__":
    run_analytical_pipeline()