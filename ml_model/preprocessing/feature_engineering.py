import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the FeatureEngineer with a calculated Pandas DataFrame.
        """
        self.df = df.copy()

    def create_lag_features(self) -> pd.DataFrame:
        """
        Create lag features for key metrics (power_kw, temperature_c, voltage) 
        to provide historical context to the ML model.
        """
        if self.df.empty:
            return self.df

        # Ensure the dataframe is sorted chronologically
        self.df = self.df.sort_values('created_at').reset_index(drop=True)

        target_columns = ['power_kw', 'temperature_c', 'voltage']

        # Create 1-step and 3-step lag features
        for col in target_columns:
            if col in self.df.columns:
                self.df[f'{col}_lag_1'] = self.df[col].shift(1)
                self.df[f'{col}_lag_3'] = self.df[col].shift(3)

        # Fill any initial NaN values caused by shifting using backward fill
        self.df = self.df.bfill()

        print("Created lag features successfully using pandas shift.")
        return self.df

    def create_rolling_features(self) -> pd.DataFrame:
        """
        Create rolling window statistics (mean and standard deviation) 
        for temperature and power to capture local trends and volatility.
        """
        if self.df.empty:
            return self.df

        window_size = 3

        if 'temperature_c' in self.df.columns:
            self.df['temp_rolling_mean'] = self.df['temperature_c'].rolling(window=window_size, min_periods=1).mean()
            self.df['temp_rolling_std'] = self.df['temperature_c'].rolling(window=window_size, min_periods=1).std().fillna(0)

        if 'power_kw' in self.df.columns:
            self.df['power_rolling_mean'] = self.df['power_kw'].rolling(window=window_size, min_periods=1).mean()
            self.df['power_rolling_std'] = self.df['power_kw'].rolling(window=window_size, min_periods=1).std().fillna(0)

        print("Created rolling window features (mean and std) successfully.")
        return self.df

    def process(self) -> pd.DataFrame:
        """
        Execute the full feature engineering pipeline: lag features and rolling statistics.
        """
        self.create_lag_features()
        self.create_rolling_features()
        return self.df
        



        