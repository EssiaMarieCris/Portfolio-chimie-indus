import numpy as np

def calculate_bias_pct(mean_measured, target):
    """
    Calcule le biais systématique en pourcentage (Justesse).
    """
    if target == 0:
        raise ValueError("La cible ne peut pas être égale à zéro.")
    return ((mean_measured - target) / target) * 100.0

def calculate_cv_pct(std_measured, mean_measured):
    """
    Calcule le coefficient de variation en pourcentage (Fidélité / Imprécision).
    """
    if mean_measured == 0:
        raise ValueError("La moyenne mesurée ne peut pas être égale à zéro.")
    return (std_measured / mean_measured) * 100.0

def calculate_total_error(bias_pct, cv_pct):
    """
    Calcule l'Erreur Totale analytique (Total Error - TE).
    Modèle standard : TE = |Biais| + 1.65 * CV%
    """
    return abs(bias_pct) + 1.65 * cv_pct

def calculate_sigma_metric(tea, bias_pct, cv_pct):
    """
    Calcule la métrique Six Sigma analytique.
    Sigma = (TEa - |Biais|) / CV%
    """
    if cv_pct == 0:
        return np.inf
    return (tea - abs(bias_pct)) / cv_pct