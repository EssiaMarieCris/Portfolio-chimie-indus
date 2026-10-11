import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_curve, auc

# 1. Chemical Dataset Simulation (QSTR Descriptors)
# Features: [MolWeight, LogP, TPSA, HBD, HBA]
np.random.seed(42)
n_compounds = 350

mol_weight = np.random.uniform(150, 650, n_compounds)
log_p = np.random.uniform(-1.0, 6.0, n_compounds)
tpsa = np.random.uniform(20, 160, n_compounds)
hbd = np.random.randint(0, 6, n_compounds)
hba = np.random.randint(1, 11, n_compounds)

X = np.column_stack([mol_weight, log_p, tpsa, hbd, hba])

# Toxicity rule-based formulation based on Lipinski and polar surface boundaries
toxic_probability = (
    (log_p > 3.0).astype(int) * 0.45
    + (tpsa < 50).astype(int) * 0.35
    + np.random.uniform(0, 0.2, n_compounds)
)
y = (toxic_probability > 0.5).astype(int)

# 2. Stratified Data Splitting
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3. Model Training
clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# 4. Evaluation Metrics
y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:, 1]

fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

print("=== DEEPTOX QSTR TOXICITY CLASSIFIER ===")
print(classification_report(y_test, y_pred, target_names=["Non-Toxic", "Toxic"]))
print(f"ROC-AUC Score: {roc_auc:.4f}")

# 5. Export ROC Curve Plot
plt.figure(figsize=(7, 5))
plt.plot(fpr, tpr, color='crimson', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=1.5, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.title('In Silico Toxicity Screening - ROC-AUC (QSTR)')
plt.legend(loc="lower right")
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('toxicity_model_roc.png', dpi=300)
print("Export completed: 'toxicity_model_roc.png'")