import os

# --- SYSTEM CONFIGURATION SWITCH ---
# Set to True when connecting to the real factory Database (production mode)
# Set to False when running local tests using simulated hardware aging data or local datasets
USE_REAL_DATABASE = False

# Database connection URL (Example for PostgreSQL, MySQL, or SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./industrial_edge.db")

# Model and scaler storage paths
MODEL_SAVE_PATH = "ml_model/training/lightgbm_base_model.pkl"
SCALER_SAVE_PATH = "ml_model/preprocessing/scaler.pkl"