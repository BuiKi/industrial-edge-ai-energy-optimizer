````markdown
# 🔄 Data Preprocessing Pipeline - Industrial Edge AI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
</p>

## 📖 Overview

The **`preprocessing`** directory serves as the core data ingestion and preparation layer for the Industrial Edge AI system. This module is responsible for asynchronously fetching raw sensor telemetry from the database, cleaning noise and anomalies, computing actual energy consumption metrics, generating advanced temporal and rolling features, and chronologically splitting the dataset to prepare it for machine learning model training.

---

## 🏗️ Component Structure

```text
preprocessing/
├── __init__.py               # Package initializer for the preprocessing pipeline
├── data_loader.py            # Asynchronously queries and loads raw sensor telemetry from PostgreSQL via SQLAlchemy
├── cleaner.py                # Cleans missing values, handles missing data, and clips physical sensor anomalies
├── calculator.py             # Computes actual energy consumption (kWh) and extracts cyclical temporal features
├── feature_engineering.py    # Generates lag features and rolling window statistics (mean & standard deviation)
├── dataset_split.py          # Performs chronological train-test splitting to prevent data leakage
└── pipeline.py               # Orchestrates all preprocessing steps into a seamless automated execution flow
```
````

---

## ⚙️ Core Module Details

1. **`DataLoader` (`data_loader.py`)**:

- Establishes asynchronous database sessions (`AsyncSession`) to query raw records efficiently.

- Retrieves time-series logs from the `sensor_data` table filtered by `device_id`.

2. **`DataCleaner` (`cleaner.py`)**:

- Drops rows missing crucial metrics (`voltage`, `power_kw`, `temperature_c`).

- Enforces strict physical safety thresholds (e.g., voltage boundaries, power limits, and operational temperatures).

3. **`DataCalculator` (`calculator.py`)**:

- Calculates actual energy consumption ($E_{\text{actual}}$ in kWh) using power values (kW) and precise time deltas between consecutive timestamps.

- Extracts cyclical temporal features such as `hour`, `day_of_week`, and `is_weekend`.

4. **`FeatureEngineer` (`feature_engineering.py`)**:

- Builds lag features (1-step and 3-step shifts) for power, temperature, and voltage metrics to provide historical context.

- Calculates rolling window statistics to capture local trends and short-term volatility.

5. **`DatasetSplitter` (`dataset_split.py`)**:

- Splits time-series data chronologically (`time_base_split`) to avoid look-ahead bias and data leakage.

6. **`PreprocessingPipeline` (`pipeline.py`)**:

- Links all the steps together sequentially, taking raw DB data and outputting clean, feature-rich training and testing sets.

---

## 🚀 Usage Example

You can integrate and execute the complete data preprocessing pipeline within your application as follows:

```python
import asyncio
from ml_model.preprocessing.pipeline import PreprocessingPipeline

async def main():
    # Initialize the pipeline with your active database session
    pipeline = PreprocessingPipeline(db_session=db_session)

    # Run the pipeline for device ID 1 with a 20% test split ratio
    train_df, test_df = await pipeline.run(device_id=1, test_size=0.2)

    print(f"Train samples: {len(train_df)}, Test samples: {len(test_df)}")

# asyncio.run(main())

```

---
