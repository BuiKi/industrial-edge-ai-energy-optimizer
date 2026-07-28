import pandas as pd 
from typing import Tuple



class DataCleaner:
    def __init__(self, df: pd.DataFrame, max_power_limit: float = 100.0, max_voltage_limit: float = 300.0):
        """
        Initialize the DataCleaner with raw dataframe and operational safety limits.
        """
        self.df = df.copy()
        self.max_power_limit = max_power_limit
        self.max_voltage_limit = max_voltage_limit

    def clean_sensor_data(self) -> pd.DataFrame:
        """
        Cleans missing values and clips physical sensor anomalies and noise spikes.
        """
        if self.df.empty:
            return self.df

        # Drop rows with critical missing values
        required_cols = ['voltage', 'power_kw', 'temperature_c']
        for col in required_cols:
            if col in self.df.columns:
                self.df = self.df.dropna(subset=[col])

        # Filter physical anomalies based on safe operational boundaries
        if 'voltage' in self.df.columns:
            self.df = self.df[(self.df['voltage'] >= 180.0) & (self.df['voltage'] <= self.max_voltage_limit)]
            
        if 'power_kw' in self.df.columns:
            self.df = self.df[(self.df['power_kw'] >= 0.0) & (self.df['power_kw'] <= self.max_power_limit)]
            
        if 'temperature_c' in self.df.columns:
            self.df = self.df[(self.df['temperature_c'] >= -10.0) & (self.df['temperature_c'] <= 150.0)]

        self.df = self.df.reset_index(drop=True)
        print(f"Data cleaning completed successfully. Remaining rows: {len(self.df)}")
        return self.df

    def process(self) -> pd.DataFrame:
        """
        Wrapper method to match pipeline execution steps.
        """
        return self.clean_sensor_data()