import numpy as np

def evaluate_westgard_rules(history_values, target, sd_nominal):
    """
    Évalue les règles de Westgard classiques sur les dernières mesures QC.
    
    Paramètres:
    - history_values : Liste ou tableau des dernières valeurs mesurées jusqu'au jour J.
    - target : Valeur cible nominale (moyenne théorique).
    - sd_nominal : Écart-type nominal (1s).
    
    Retourne:
    - dict : Statut des violations et liste des règles enfreintes.
    """
    history = np.asarray(history_values)
    n = len(history)
    if n == 0:
        return {"rejection": False, "warning": False, "violations": []}
    
    violations = []
    rejection = False
    warning = False
    
    current_val = history[-1]
    z_score = (current_val - target) / sd_nominal
    
    # Règle 1_2s (Avertissement)
    if abs(z_score) > 2.0:
        warning = True
        violations.append("1_2s (Avertissement : Z > 2s)")
        
    # Règle 1_3s (Rejet - Erreur aléatoire majeure)
    if abs(z_score) > 3.0:
        rejection = True
        violations.append("1_3s (Rejet critique : Z > 3s)")
        
    # Règle 2_2s (Rejet - Erreur systématique)
    if n >= 2:
        z_prev = (history[-2] - target) / sd_nominal
        if (z_score > 2.0 and z_prev > 2.0) or (z_score < -2.0 and z_prev < -2.0):
            rejection = True
            violations.append("2_2s (Rejet systématique : 2 consécutifs > 2s)")
            
    # Règle 10_x (Rejet / Alerte - Dérive de justesse)
    if n >= 10:
        last_10 = history[-10:]
        if np.all(last_10 > target) or np.all(last_10 < target):
            rejection = True
            violations.append("10_x (Rejet : 10 consécutifs du même côté de la moyenne)")
            
    return {
        "rejection": rejection,
        "warning": warning,
        "violations": violations
    }