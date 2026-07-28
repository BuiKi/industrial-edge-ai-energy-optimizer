import os
import psutil
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error

class SystemValidator:
    def __init__(self, max_cpu_percent: float = 80.0, max_threads: int = 2):
        """
        Initialize the system validator and resource limiter.
        :param max_cpu_percent: Maximum allowable CPU usage percentage before raising a warning.
        :param max_threads: Maximum number of CPU threads allocated for background tasks.
        """
        self.max_cpu_percent = max_cpu_percent
        self.max_threads = max_threads

        # Enforce thread limit for background AI tasks to protect real-time API performance
        os.environ["OMP_NUM_THREADS"] = str(max_threads)
        os.environ["MKL_NUM_THREADS"] = str(max_threads)
        os.environ["OPENBLAS_NUM_THREADS"] = str(max_threads)

    def validate_model_performance(self, y_true: np.ndarray, y_preb: np.ndarray) -> dict:
        """
        Comprehensive evaluation of model performance using RMSE and MAE.
        """
        rmse = np.sqrt(mean_squared_error(y_true, y_preb))
        mae = mean_absolute_error(y_true, y_preb)

        # Check current system resource utilization
        current_cpu_usage = psutil.cpu_percent(interval=0.1)
        is_cpu_overloaded = current_cpu_usage > self.max_cpu_percent

        validation_report = {
            "rmse": float(rmse),
            "mae": float(mae),
            "cpu_usage_percent": float(current_cpu_usage),
            "cpu_overloaded": bool(is_cpu_overloaded),
            "status": "Warning: CPU resource limit exceeded, potential risk to real-time API!" if is_cpu_overloaded else "System resources and model performance are within optimal limits."
        }

        return validation_report


   
