import os
import numpy as np
import pandas as pd

from metrics import calculate_bias_pct, calculate_cv_pct, calculate_total_error, calculate_sigma_metric
from predictor import predict_drift_and_rul
from calibrator import fit_calibration_curve, diagnose_calibration_drift
from westgard import evaluate_westgard_rules

def run_analytical_pipeline():
    # 1. Chargement des séries temporelles
    data_path = os.path.join(os.path.dirname(__file__), "../data/qc_measurements.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError("Exécutez data_generator.py pour créer les données.")
        
    df = pd.read_csv(data_path)
    days = df["day"].values
    measured = df["measured"].values
    target = df["target"].iloc[0]
    
    tea = 6.0  # Erreur Totale Admissible (6.0%)
    sd_nominal = target * (2.0 / 100.0)  # SD pour un CV nominal de 2%
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
        
    # 3. Diagnostic comparatif au Jour 18
    day_diag = 18
    w_start = day_diag - fenetre
    
    # Évaluation rétrospective (Westgard)
    westgard_status = evaluate_westgard_rules(measured[:day_diag], target, sd_nominal)
    
    # Évaluation prédictive (RUL & Total Error)
    pente, ordonnee, rul, _ = predict_drift_and_rul(
        days[w_start:day_diag],
        total_errors[w_start:day_diag],
        threshold=tea,
        current_day=day_diag
    )
    
    # Diagnostic d'étalonnage physique
    std_conc = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    abs_j1 = 0.450 * std_conc + 0.010
    slope_init, int_init, _ = fit_calibration_curve(std_conc, abs_j1)
    
    abs_diag = (0.450 * 0.82) * std_conc + 0.022  # Dégradation optique
    slope_curr, int_curr, _ = fit_calibration_curve(std_conc, abs_diag)
    diag_res = diagnose_calibration_drift(slope_init, slope_curr, int_init, int_curr)
    
    # 4. Rapport d'audit comparatif
    print("==================================================")
    print(" RAPPORT MÉTROLOGIQUE COMPARATIF (JOUR 18)")
    print("==================================================")
    print(f"Erreur Totale mesurée         : {total_errors[day_diag-1]:.2f}% (TEa max: {tea}%)")
    print(f"Indice Six Sigma              : {sigma_scores[day_diag-1]:.2f} σ")
    print("--- CONTRÔLE STATISTIQUE RÉTROSPECTIF (WESTGARD) ---")
    print(f"Statut Rejet immédiat         : {'OUI' if westgard_status['rejection'] else 'NON'}")
    print(f"Statut Avertissement          : {'OUI' if westgard_status['warning'] else 'NON'}")
    violations_str = ", ".join(westgard_status["violations"]) if westgard_status["violations"] else "Aucune"
    print(f"Règles enfreintes             : {violations_str}")
    print("--- SURVEILLANCE PRÉDICTIVE PROACTIVE ---")
    print(f"Dérive estimée                : +{pente:.3f}% TE/jour")
    print(f"Horizon critique (RUL)        : {rul:.1f} jours avant non-conformité TEa")
    print(f"Diagnostic matériel           : {diag_res['diagnosis']}")
    print(f"Action corrective             : {'[RÉÉTALONNAGE PROGRAMMÉ]' if diag_res['needs_recalibration'] else '[AUCUNE]'}")
    print("==================================================")

if __name__ == "__main__":
    run_analytical_pipeline()