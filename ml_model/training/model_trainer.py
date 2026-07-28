import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
from typing import Dict, Any

class ModelTrainer:
    def __init__(self, params: Dict[str, Any] = None):
        """
        Initialize the ModelTrainer with production-grade hyperparameters.
        Optimized for robust noise tolerance and strict CPU resource control on edge devices.
        """
        self.params = params or {
            'objective': 'huber',             # Use Huber Loss to neutralize residual sensor noise and outliers
            'alpha': 0.95,                    # Quantile parameter for Huber loss smooth transition
            'metric': 'rmse',                 # Root Mean Squared Error for performance tracking
            'boosting_type': 'gbdt',          # Gradient Boosting Decision Tree framework
            'learning_rate': 0.05,            # Controlled step size for stable convergence
            'num_leaves': 31,                 # Maximum tree leaves for complex pattern recognition
            'max_depth': -1,                  # Unconstrained depth, controlled by num_leaves
            'n_estimators': 1000,             # Maximum boosting rounds ceiling
            'random_state': 42,               # Ensure deterministic and reproducible results
            'n_jobs': 2                       # Restrict CPU threads to prevent blocking real-time API telemetry ingestion
        }
        self.model = None

    def train(self, train_df: pd.DataFrame, target_col: str = 'E_actual') -> lgb.LGBMRegressor:
        """
        Execute chronological time-series cross-validation training pipeline 
        to prevent future data leakage.
        """
        # Safety check: Ensure the dataset is not empty
        if train_df.empty:
            raise ValueError("Training dataframe is empty. Cannot proceed with model training.")

        # Safety check: Ensure target feature exists in dataset
        if target_col not in train_df.columns:
            raise ValueError(f"Target column '{target_col}' not found in training dataframe.")

        # Separate feature matrix (X) and target variable (y), dropping non-feature columns
        drop_cols = [target_col, 'created_at']
        X = train_df.drop(columns=[col for col in drop_cols if col in train_df.columns], errors='ignore')
        y = train_df[target_col]

        # Initialize TimeSeriesSplit to respect chronological order (past predicting future)
        tscv = TimeSeriesSplit(n_splits=5)
        
        cv_scores = []
        best_model = None
        best_score = float('inf')

        print("--- STARTING TIME-SERIES CROSS-VALIDATION TRAINING ---")
        
        # Iterating through chronological folds
        for fold, (train_index, val_index) in enumerate(tscv.split(X)):
            X_train, X_val = X.iloc[train_index], X.iloc[val_index]
            y_train, y_val = y.iloc[train_index], y.iloc[val_index]

            # Instantiate LightGBM Regressor for the current fold
            model = lgb.LGBMRegressor(**self.params)

            # Fit the model with early stopping to prevent overfitting
            model.fit(
                X_train, y_train,
                eval_set=[(X_val, y_val)],
                callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)]
            )

            # Evaluate model performance on validation split using RMSE
            preds = model.predict(X_val)
            rmse = np.sqrt(mean_squared_error(y_val, preds))
            cv_scores.append(rmse)
            
            print(f"Fold {fold + 1} Validation RMSE: {rmse:.4f}")

            # Track and retain the best performing model across all folds
            if rmse < best_score:
                best_score = rmse
                best_model = model

        print(f"Training completed successfully. Average CV RMSE: {np.mean(cv_scores):.4f}")
        self.model = best_model
        return self.model

    def save_model(self, file_path: str = "ml_model/training/lightgbm_model.txt"):
        """
        Serialize and save the trained model artifact to disk for downstream inference pipelines.
        """
        if self.model is not None:
            self.model.booster_.save_model(file_path)
            print(f"Model artifact successfully saved to: {file_path}")
        else:
            print("Warning: No trained model available to save.")