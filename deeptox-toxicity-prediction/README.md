# In Silico Toxicity Prediction Pipeline (QSTR Modeling)

## Industrial Objective & Regulatory Scope
During early drug discovery, evaluating candidate toxicity *in silico* reduces late-stage clinical attrition and supports the **3Rs principles** (Replacement, Reduction, Refinement of animal testing) per **ICH M7** and **OECD** guidelines.

This module implements a Quantitative Structure-Toxicity Relationship (**QSTR**) classifier leveraging physicochemical molecular descriptors.

---

## Molecular Descriptors & Feature Space
* **Molecular Weight (MW)**: Size and bioaccumulation determinant (150 - 650 g/mol).
* **LogP (Octanol-Water Partition Coefficient)**: Membrane permeability and lipophilicity indicator.
* **TPSA (Topological Polar Surface Area)**: Cellular bioavailability and passive transport constraint.
* **Hydrogen Bond Donors/Acceptors (HBD / HBA)**: Electrostatic receptor interaction parameters.

---

## Machine Learning Classifier
* **Algorithm**: Random Forest Classifier (100 estimators).
* **Validation Strategy**: Stratified Split (75% Train / 25% Test).
* **Performance Metric**: Area Under the Receiver Operating Characteristic curve (**ROC-AUC**), sensitivity, and specificity.

---

## Deliverables
* `train_model.py`: Pipeline execution script.
* `toxicity_model_roc.png`: Output ROC curve visual.
* `README.md`: Module documentation and industrial context.