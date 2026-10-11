import sys
import os
import pytest

# Ajout du dossier src au chemin d'importation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from metrics import calculate_bias_pct, calculate_cv_pct, calculate_total_error, calculate_sigma_metric

def test_calculate_bias_pct():
    # Cible = 1.00 g/L, Mesuré = 1.02 g/L -> Biais attendu = +2.0%
    bias = calculate_bias_pct(1.02, 1.00)
    assert pytest.approx(bias, rel=1e-3) == 2.0

def test_calculate_cv_pct():
    # Moyenne = 1.00 g/L, Écart-type = 0.03 g/L -> CV% attendu = 3.0%
    cv = calculate_cv_pct(0.03, 1.00)
    assert pytest.approx(cv, rel=1e-3) == 3.0

def test_calculate_total_error():
    # Biais = 2.0%, CV = 2.0% -> TE = 2.0 + 1.65 * 2.0 = 5.3%
    te = calculate_total_error(2.0, 2.0)
    assert pytest.approx(te, rel=1e-3) == 5.3

def test_calculate_sigma_metric():
    # TEa = 6.0%, Biais = 1.0%, CV = 1.0% -> Sigma = (6.0 - 1.0) / 1.0 = 5.0
    sigma = calculate_sigma_metric(6.0, 1.0, 1.0)
    assert pytest.approx(sigma, rel=1e-3) == 5.0