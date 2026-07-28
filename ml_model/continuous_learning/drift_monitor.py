import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

class DriftMonitor:
    def __init__(self, rmse_threshold: float = 1.5):
        """
        Initialize the Concept Drift Monitor.
        :param rmse_threshold: Maximum allowable RMSE threshold. 
                               If the actual RMSE exceeds this value, a drift warning is triggered.
        """
        self.rmse_threshold = rmse_threshold

    def evaluate_drift(self, y_true: np.ndarray, y_pred: np.ndarray) -> dict:
        """
        Evaluate the deviation between true labels and model predictions on new incoming data.
        """
        # Calculate current Root Mean Squared Error (RMSE)
        current_rmse = np.sqrt(mean_squared_error(y_true, y_pred))

        # Check if error exceeds the safety threshold
        is_drift_detected = current_rmse > self.rmse_threshold

        status_report = {
            "current_rmse": float(current_rmse),
            "threshold": self.rmse_threshold,
            "dift_detected": bool(is_drift_detected),
            "message": "Warning: Model concept drift detected due to hardware degradation!" if is_drift_detected else "Model is operating stably within safe parameters."
        }
        return status_report