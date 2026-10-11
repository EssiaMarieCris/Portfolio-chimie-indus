# Pharmaceutical Chemometrics: NIR Spectral Preprocessing & PCA Pipeline

## Context & Industrial Objective
In solid oral dosage manufacturing, raw material verification and batch-to-batch monitoring must adhere to **Process Analytical Technology (PAT)** and **ICH Q8** regulatory guidelines. 

This project demonstrates a multi-phase chemometric workflow applied to Near-Infrared (NIR) diffuse reflectance spectra to discriminate Active Pharmaceutical Ingredients (APIs) from excipients, overcoming physical particle scattering.

---

## Phase 1: Data Acquisition & Spectral Simulation
* **Objective**: Simulate non-destructive NIR absorption spectra representing typical pharmaceutical powders.
* **Spectral Window**: $1100 - 2200 \text{ nm}$ capturing characteristic overtone and combination vibrational bands ($\text{C-H}$, $\text{O-H}$, $\text{N-H}$).
* **Formulation Classes**:
  * `API-A`: Peak centered at $1450 \text{ nm}$ ($n = 30$)
  * `API-B`: Peak centered at $1650 \text{ nm}$ ($n = 30$)
  * `Excipient`: Binder/filler matrix centered at $1900 \text{ nm}$ ($n = 30$)
* **Physical Artifacts**: Introduced additive baseline shifts and multiplicative light scattering mimicking varied particle size distributions.

---

## Phase 2: Chemometric Preprocessing (Scatter Correction)
* **Objective**: Isolate chemical variance from physical scattering artifacts without distorting intrinsic molecular signals.
* **Algorithm**: **Standard Normal Variate (SNV)**.
* **Mathematical Model**:
  $$\mathbf{x}_{\text{corr}} = \frac{\mathbf{x} - \mu}{\sigma}$$
  * $\mu$: Sample mean absorbance across the spectral range.
  * $\sigma$: Sample standard deviation across the spectral range.
* **Yield**: Eliminates baseline slope and offset drift on a per-spectrum basis without requiring external calibration standards.

---

## Phase 3: Unsupervised Multivariate Modeling (PCA)
* **Objective**: Dimensionality reduction and unsupervised pattern recognition across collinear spectral bands.
* **Method**: Principal Component Analysis (PCA) via Singular Value Decomposition (SVD) on mean-centered SNV data.
* **Latent Variables**: 2 orthogonal Principal Components retained.

---

## Phase 4: Validation & Quantitative Results
* **Explained Variance**:
  * **PC1**: $49.60\%$
  * **PC2**: $49.52\%$
  * **Cumulative Explained Variance**: $\mathbf{99.12\%}$
* **Clustering Analysis**: Complete, distinct separation between `API-A`, `API-B`, and `Excipient` with zero cluster overlap.
* **Graphical Deliverable**: Score plot generated and exported as `pca_chemometrics_result.png`.

---

## Phase 5: Reproducibility & Deployment
* **Prerequisites**: Python 3.10+ (`deeptox` Conda environment), `numpy`, `scipy`, `scikit-learn`, `matplotlib`.
* **Execution**:
  ```bash
  python analysis.py