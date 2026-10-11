import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 1. توليد بيانات طيفية صيدلانية محاكية (NIR Spectra)
np.random.seed(42)
wavelengths = np.linspace(1100, 2200, 200)

def generate_spectrum(base_peak, noise_level=0.02):
    absorbance = np.exp(-((wavelengths - base_peak) ** 2) / (2 * 40 ** 2))
    noise = np.random.normal(0, noise_level, len(wavelengths))
    scatter_effect = np.random.uniform(0.1, 0.5)
    return absorbance + noise + scatter_effect

# دمج عينات: مادة فعالة A، مادة فعالة B، وسواغ (Excipient)
samples = []
labels = []

for _ in range(30):
    samples.append(generate_spectrum(1450)) # API A
    labels.append("API-A")
for _ in range(30):
    samples.append(generate_spectrum(1650)) # API B
    labels.append("API-B")
for _ in range(30):
    samples.append(generate_spectrum(1900)) # Excipient
    labels.append("Excipient")

X = np.array(samples)

# 2. المعالجة القبلية: خوارزمية SNV (Standard Normal Variate)
def apply_snv(spectral_data):
    mean_corrected = spectral_data - np.mean(spectral_data, axis=1, keepdims=True)
    return mean_corrected / np.std(spectral_data, axis=1, keepdims=True)

X_snv = apply_snv(X)

# 3. تحليل المكونات الرئيسية (PCA)
pca = PCA(n_components=2)
scores = pca.fit_transform(X_snv)

print(f"Variance explained PC1: {pca.explained_variance_ratio_[0]*100:.2f}%")
print(f"Variance explained PC2: {pca.explained_variance_ratio_[1]*100:.2f}%")

# 4. حفظ النتائج بصرياً
plt.figure(figsize=(9, 5))
for label, color in [("API-A", "blue"), ("API-B", "green"), ("Excipient", "red")]:
    idx = [i for i, lbl in enumerate(labels) if lbl == label]
    plt.scatter(scores[idx, 0], scores[idx, 1], label=label, c=color, alpha=0.7)

plt.title("Chemometrics: PCA Score Plot of Raw Materials")
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
plt.legend()
plt.grid(True)
plt.savefig("pca_chemometrics_result.png")
print("Analysis complete. Plot saved as 'pca_chemometrics_result.png'.")