# Chemical Hazard & CLP Pictogram Detector

Système déterministe d'identification visuelle des pictogrammes de danger CLP/SGH et d'interrogation toxicologique automatisée via registres officiels (INRS & PubChem).

Projet réalisé dans le cadre du cursus de Master Chimie Industrielle.

---

## 1. Présentation générale

Ce module assure deux fonctions critiques en hygiène, sécurité et environnement (HSE) :
1. **Reconnaissance visuelle de pictogrammes CLP (GHS01 à GHS09)** à partir d'échantillons d'images (JPEG, PNG) par extraction de gabarits et analyse d'intersection structurelle (IoU / corrélation croisée normalisée).
2. **Génération de fiches de sécurité toxicologiques** via requête directe sur l'API publique de PubChem (National Library of Medicine) croisée avec les prescriptions de stockage de l'INRS (Institut National de Recherche et de Sécurité).

---

## 2. Architecture du projet

```text
chemical-hazard-detector/
├── data/
│   ├── hazards.json           # Référentiel réglementaire officiel INRS (GHS01 à GHS09)
│   └── templates/              # Gabarits visuels de référence (PNG calibrés)
├── src/
│   ├── image_detector.py      # Moteur d'analyse visuelle et d'alignement géométrique
│   └── chemical_lookup.py     # Module d'extraction toxicologique par API REST
├── requirements.txt           # Dépendances logicielles
└── README.md                  # Documentation technique
3. Spécifications techniques
Langage : Python 3.10+

Vision par ordinateur : OpenCV (cv2) — Prétraitement morphologique (seuillage binaire inverse, rognage centré), corrélation croisée normalisée (TM_CCOEFF_NORMED) et indice d'intersection sur union (IoU).

Interrogation API : urllib.request — Requêtes REST PUG View vers le registre officiel PubChem.

Cadre réglementaire : Règlement CE n° 1272/2008 (CLP) et recommandations de stockage INRS.

4. Installation et exécution
Prérequis

Installer les bibliothèques requises :

pip install opencv-python numpy

Module 1 : Détection visuelle d'un pictogramme
Pour classifier une image de danger (ex. silhouet.jpg, format PNG/JPEG) et obtenir le rapport de danger associé :


python src/image_detector.py
Saisir le chemin relatif de l'image lors de l'invite.

Module 2 : Recherche de fiche toxicologique
Pour interroger le registre officiel pour une entité chimique donnée (ex. Acetone, Benzene, Sulfuric acid) :


python src/chemical_lookup.py

5. Référentiels et sources

INRS : Classification CLP et étiquetage des produits chimiques.

PubChem : Base de données publique de composés chimiques (NIH / NLM).