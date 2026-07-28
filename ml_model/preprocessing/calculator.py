import pandas as pd
import numpy as np

class DataCalculator():
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DataCalculator with a cleaned Pandas DataFrame.
        """
        self.df = df.copy()

    def calculate_actual_energy(self) -> pd.DataFrame:
        """
        Calculate actual energy consumption (E_actual) based on power (kW) 
        and the time interval (delta time in hours) between consecutive records.
        """
        if self.df.empty or 'created_at' not in self.df.columns or 'power_kw' not in self.df.columns:
            return self.df

        # Ensure power_kw column is numeric to prevent type conflicts
        self.df['power_kw'] = pd.to_numeric(self.df['power_kw'], errors='coerce')

        # Ensure the dataframe is sorted by time
        self.df = self.df.sort_values('created_at').reset_index(drop=True)

        # Calculate time difference in hours between consecutive rows
        time_diff_hours = self.df['created_at'].diff().dt.total_seconds().fillna(0) / 3600.0

        # Energy (kWh) = Power (kW) * Time (hours)
        self.df['energy_actual_kwh'] = self.df['power_kw'] * time_diff_hours

        # Handle the first row's energy by backfilling with the second row's time delta if available
        if len(self.df) > 1 and time_diff_hours.iloc[1] > 0:
            target_col = 'energy_actual_kwh' if 'energy_actual_kwh' in self.df.columns else 'energy_actual_kw'
            # Use .loc with integer index instead of .iloc with string column name to avoid TypeError
            self.df.loc[0, target_col] = self.df.loc[0, 'power_kw'] * time_diff_hours.iloc[1]

        print("Calculated actual energy consumption (energy_actual_kwh) successfully.")
        return self.df

    def extract_time_features(self) -> pd.DataFrame:
        """
        Extract basic temporal features from the 'created_at' timestamp 
        to help the AI model capture cyclical patterns (e.g., hour of day, day of week).
        """
        if self.df.empty or 'created_at' not in self.df.columns:
            return self.df

        # Ensure created_at is in datetime format
        self.df['created_at'] = pd.to_datetime(self.df['created_at'], errors='coerce')

        # Extract useful calendar/time attributes
        self.df['hour'] = self.df['created_at'].dt.hour
        self.df['day_of_week'] = self.df['created_at'].dt.dayofweek
        self.df['is_weekend'] = self.df['day_of_week'].isin([5, 6]).astype(int)

        print("Extracted basic temporal features (hour, day_of_week, is_weekend) successfully.")
        return self.df

    def process(self) -> pd.DataFrame:
        """
        Execute the calculation pipeline: compute actual energy and extract time features.
        """
        self.calculate_actual_energy()
        self.extract_time_features()
        return self.df