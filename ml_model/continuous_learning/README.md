````markdown
# 🔄 Continuous Learning & Drift Monitoring - Industrial Edge AI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/LightGBM-EB6841?style=for-the-badge&logo=lightgbm&logoColor=white" alt="LightGBM" />
  <img src="https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" />
</p>

## 📖 Overview

The **`continuous_learning`** directory is responsible for maintaining model accuracy and adaptability over time in dynamic industrial environments. This module detects concept drift caused by hardware wear-and-tear or changing operating patterns and performs incremental fine-tuning (warm-start training) without retraining the model from scratch[cite: 8, 9].

---

## 🏗️ Component Structure

```text
continuous_learning/
├── __init__.py      # Package initializer for the continuous learning module
├── drift_monitor.py # Evaluates incoming telemetry against true labels to detect model performance degradation
└── fine_tuner.py    # Loads existing model weights and performs incremental fine-tuning on new incoming data
```
````

---

## ⚙️ Core Module Details

1. **`DriftMonitor` (`drift_monitor.py`)**:

- Computes real-time Root Mean Squared Error (RMSE) between model predictions and true observed values.

- Triggers drift warnings when prediction errors exceed predefined safety thresholds (indicating potential hardware degradation).

2. **`ModelFineTuner` (`fine_tuner.py`)**:

- Loads pre-trained LightGBM model checkpoints from disk (`init_model`) to preserve historical learning.

- Executes incremental training (`warm-start`) using new incoming data streams with controlled learning rates and boosting rounds to adapt to shifting industrial conditions.

- Provides artifact persistence to save re-weighted models back to disk.

---

## 🚀 Usage Example

You can integrate drift detection and model fine-tuning into your edge inference loop as follows:

```python
import numpy as np
import pandas as pd
from ml_model.continuous_learning.drift_monitor import DriftMonitor
from ml_model.continuous_learning.fine_tuner import ModelFineTuner

# 1. Monitor for Concept Drift
monitor = DriftMonitor(rmse_threshold=1.5)
status = monitor.evaluate_drift(y_true, y_pred)

if status["dift_detected"]:
    print(status["message"])

    # 2. Fine-tune model incrementally if drift occurs
    fine_tuner = ModelFineTuner(model_path="ml_model/training/lightgbm_model.txt")
    updated_model = fine_tuner.fine_tune(X_new, y_new, learning_rate=0.01, num_boost_round=50)

    # 3. Save the updated model
    fine_tuner.save_updated_model("ml_model/training/lightgbm_model.txt")

```

---
