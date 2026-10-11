import numpy as np

def predict_drift_and_rul(days_window, values_window, threshold, current_day):
    """
    Calcule la pente de dérive par régression linéaire et estime
    le nombre de jours restants avant rupture (RUL : Remaining Useful Life).
    
    Paramètres:
    - days_window : Tableau des jours de la fenêtre d'observation.
    - values_window : Tableau des valeurs observées sur cette fenêtre.
    - threshold : Seuil critique à ne pas franchir (ex: limite +2s ou TEa).
    - current_day : Jour actuel d'analyse.
    
    Retourne:
    - slope : Vitesse de dérive par jour.
    - intercept : Ordonnée à l'origine.
    - rul : Jours restants avant dépassement (np.inf si pas de dérive vers le seuil).
    - projected_day : Jour calendaire prévu pour le franchissement.
    """
    if len(days_window) < 2:
        raise ValueError("Au moins 2 points sont requis pour calculer une tendance.")
        
    slope, intercept = np.polyfit(days_window, values_window, 1)
    
    # Si la pente monte vers un seuil supérieur
    if slope > 0:
        projected_day = (threshold - intercept) / slope
        rul = projected_day - current_day
        if rul < 0:
            rul = 0.0  # Déjà franchi
    else:
        rul = np.inf
        projected_day = np.inf
        
    return slope, intercept, rul, projected_day