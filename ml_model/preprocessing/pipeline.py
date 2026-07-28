import pandas as pd 
from typing import Tuple

from ml_model.preprocessing.data_loader import DataLoader
from ml_model.preprocessing.cleaner import DataCleaner
from ml_model.preprocessing.calculator import DataCalculator
from ml_model.preprocessing.feature_engineering import FeatureEngineer
from ml_model.preprocessing.dataset_split import DatasetSplitter

class PreprocessingPipeline:
    def __init__(self, db_session=None):
        """
        Initialize the pipeline with an active database asynchronous session.
        """
        self.db_session = db_session

    async def run(self, device_id: int = 1, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Execute the full preprocessing pipeline from raw data loading to final dataset splitting.
        """
        print(f"--- STARTING PREPROCESSING PIPELINE FOR DEVICE_ID: {device_id} ---")

        # Step 1: Load raw data from database 
        loader = DataLoader(self.db_session)
        raw_df = await loader.load_telemetry_data(device_id=device_id)

        if raw_df.empty:
            print(f"Warning: Raw dataframe is empty for device_id {device_id}. Pipeline stopped.")
            return pd.DataFrame(), pd.DataFrame()

        # Step 2: Clean missing values and outliers
        cleaner = DataCleaner(raw_df)
        cleaned_df = cleaner.process()

        # Step 3: Calculate actual energy and time features
        calculator = DataCalculator(cleaned_df)
        calculated_df = calculator.process()

        # Step 4: Feature Engineering (Lag & Rolling features)
        engineer = FeatureEngineer(calculated_df)
        featured_df = engineer.process()

        # Step 5: Chronological Train/Test Split
        splitter = DatasetSplitter(featured_df)
        train_df, test_df = splitter.time_base_split(test_size=test_size)

        print("--- PREPROCESSING PIPELINE COMPLETED SUCCESSFULLY ---")
        return train_df, test_df