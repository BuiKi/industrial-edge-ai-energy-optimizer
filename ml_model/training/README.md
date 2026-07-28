````markdown
# 🤖 Model Training Pipeline - Industrial Edge AI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/LightGBM-EB6841?style=for-the-badge&logo=lightgbm&logoColor=white" alt="LightGBM" />
  <img src="https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" />
</p>

## 📖 Overview

The **`training`** directory handles the machine learning model lifecycle for the Industrial Edge AI system. It implements a robust, edge-optimized training pipeline utilizing **LightGBM** with Huber Loss for noise resilience[cite: 7]. The architecture strictly adheres to chronological time-series cross-validation to prevent data leakage and ensure reliable predictive performance on industrial telemetry[cite: 7].

---

## 🏗️ Component Structure

```text
training/
├── __init__.py         # Package initializer for the training module
└── trainer.py          # Contains the ModelTrainer class for cross-validation, hyperparameter tuning, and serialization
```
````

---

## ⚙️ Core Module Details

1. **`ModelTrainer` (`trainer.py`)**:

- **Edge-Optimized Hyperparameters:** Pre-configured with resource constraints (e.g., restricted `n_jobs=2` threads) to prevent blocking real-time API telemetry ingestion on edge hardware.

- **Noise Tolerance:** Employs `Huber Loss` with an alpha quantile of $0.95$ to neutralize residual sensor noise and outliers common in factory environments.

- **Chronological Validation:** Uses Scikit-Learn's `TimeSeriesSplit` (5 folds) to simulate real-world forecasting conditions without future data leakage.

- **Early Stopping & Persistence:** Integrates early stopping rounds to prevent overfitting and provides native model artifact serialization (`save_model`) for downstream inference.

---

## 🚀 Usage Example

You can initialize and run the training process within your pipeline as follows:

```python
import pandas as pd
from ml_model.training.trainer import ModelTrainer

# Assume 'train_df' is the processed dataset from your preprocessing pipeline
trainer = ModelTrainer()

# Train the LightGBM model using chronological cross-validation
trained_model = trainer.train(train_df, target_col='energy_actual_kwh')

# Save the trained model artifact to disk
trainer.save_model(file_path="ml_model/training/lightgbm_model.txt")

```

---
