import pandas as pd
from typing import Tuple

class DatasetSplitter:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DatasetSplitter with a fully processed Pandas DataFrame.
        """
        self.df = df.copy()

    def time_base_split(self, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split the time-series dataframe into training and testing sets chronologically 
        to prevent data leakage.
        """
        if self.df.empty:
            return pd.DataFrame(), pd.DataFrame()

        # Ensure the dataframe is strictly sorted by time
        self.df = self.df.sort_values('created_at').reset_index(drop=True)

        # Calculate the split index based on the test_size ratio
        split_index = int(len(self.df) * (1 - test_size))

        # Split chronologically
        train_df = self.df.iloc[:split_index].copy()
        test_df = self.df.iloc[split_index:].copy()

        print(f"Dataset split successfully: Train set ({len(train_df)} rows), Test set ({len(test_df)} rows).")
        return train_df, test_df