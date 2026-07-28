````markdown
# 🛡️ System Validation & Resource Monitoring - Industrial Edge AI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Psutil-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Psutil" />
  <img src="https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" />
</p>

## 📖 Overview

The **`validation`** directory ensures system stability and evaluation integrity for the Industrial Edge AI framework. This module is responsible for performing comprehensive accuracy evaluations (RMSE and MAE) while simultaneously monitoring edge hardware resource utilization (CPU limits and thread allocation) to safeguard real-time API performance[cite: 10].

---

## 🏗️ Component Structure

```text
validation/
├── __init__.py     # Package initializer for the validation module
└── validator.py    # Contains the SystemValidator class for performance metrics tracking and resource constraint enforcement
```
````

---

## ⚙️ Core Module Details

1. **`SystemValidator` (`validator.py`)**:

- **Resource Limiter:** Enforces strict CPU thread limits (`OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`) upon initialization to prevent background AI tasks from blocking real-time API telemetry ingestion.

- **Performance Evaluation:** Calculates core regression metrics including Root Mean Squared Error (RMSE) and Mean Absolute Error (MAE).

- **Hardware Overload Monitoring:** Tracks live CPU usage percentages using `psutil` and triggers warnings if utilization exceeds safe operational boundaries.

---

## 🚀 Usage Example

You can integrate system validation and resource tracking into your production execution loop as follows:

```python
import numpy as np
from ml_model.validation.validator import SystemValidator

# Initialize system validator with custom thresholds (e.g., max 80% CPU usage, max 2 threads)
validator = SystemValidator(max_cpu_percent=80.0, max_threads=2)

# Run performance and resource validation
report = validator.validate_model_performance(y_true, y_pred)

print(f"RMSE: {report['rmse']:.4f}")
print(f"MAE: {report['mae']:.4f}")
print(f"CPU Usage: {report['cpu_usage_percent']}%")
print(report['status'])

```

---
