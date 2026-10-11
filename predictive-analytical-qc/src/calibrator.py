import numpy as np

def fit_calibration_curve(concentrations, absorbances):
    """
    Ajuste une droite d'étalonnage par la méthode des moindres carrés (A = a*C + b).
    
    Retourne:
    - slope : Sensibilité analytique (pente a).
    - intercept : Signal du blanc / ordonnée à l'origine (b).
    - r_squared : Coefficient de détermination R².
    """
    concentrations = np.asarray(concentrations)
    absorbances = np.asarray(absorbances)
    
    slope, intercept = np.polyfit(concentrations, absorbances, 1)
    
    # Calcul du coefficient de détermination R²
    y_pred = slope * concentrations + intercept
    ss_res = np.sum((absorbances - y_pred) ** 2)
    ss_tot = np.sum((absorbances - np.mean(absorbances)) ** 2)
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0
    
    return slope, intercept, r_squared

def diagnose_calibration_drift(slope_initial, slope_current, intercept_initial, intercept_current, threshold_loss_pct=10.0):
    """
    Diagnostique l'origine instrumentale de la dérive métrologique.
    """
    loss_slope_pct = ((slope_initial - slope_current) / slope_initial) * 100.0
    delta_intercept = intercept_current - intercept_initial
    
    needs_recalibration = False
    reasons = []
    
    if loss_slope_pct >= threshold_loss_pct:
        needs_recalibration = True
        reasons.append(f"Perte critique de sensibilité optique (-{loss_slope_pct:.1f}%)")
        
    if abs(delta_intercept) > 0.010:  # Dérive de fond significative
        needs_recalibration = True
        reasons.append(f"Dérive du zéro / encrassement optique (Δb = {delta_intercept:+.4f} UA)")
        
    return {
        "needs_recalibration": needs_recalibration,
        "loss_slope_pct": loss_slope_pct,
        "delta_intercept": delta_intercept,
        "diagnosis": " | ".join(reasons) if reasons else "Paramètres nominaux conformes"
    }