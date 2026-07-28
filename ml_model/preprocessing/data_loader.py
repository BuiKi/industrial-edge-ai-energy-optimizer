import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class DataLoader:
    def __init__(self, db_session: AsyncSession):
        """
        Initialize the DataLoader with an active database asynchronous session.
        """
        self.db_session = db_session

    async def load_telemetry_data(self, device_id: int, limit: int = 10000) -> pd.DataFrame:
        """
        Query raw sensor telemetry data from PostgreSQL based on device_id 
        and convert the result into a Pandas DataFrame.
        """
        # SQL query targeting the actual 'sensor_data' table and its columns
        query = text("""
            SELECT id, device_id, power_kw, temperature_c, voltage, optimal_baseline, is_anomaly, created_at
            FROM sensor_data
            WHERE device_id = :device_id
            ORDER BY created_at ASC
            LIMIT :limit;
        """)

        # Execute the asynchronous query using SQLAlchemy
        result = await self.db_session.execute(query, {"device_id": device_id, "limit": limit})
        rows = result.fetchall()

        # Define column schema to return an empty DataFrame if no record are found 
        columns = ['id', 'device_id', 'power_kw', 'temperature_c', 'voltage', 'optimal_baseline', 'is_anomaly', 'created_at']

        if not rows:
            print(f"No telemetry data found for device_id = {device_id}")
            return pd.DataFrame(columns=columns)

        # Convert fetched rows into a Pandas DataFrame
        df = pd.DataFrame(rows, columns=columns)
        
        # Ensure the timestamp column is parsed as Pandas datetime for downstream time-series processing
        df['created_at'] = pd.to_datetime(df['created_at'])

        print(f"Successfully loaded {len(df)} telemetry rows for device_id = {device_id}")
        return df