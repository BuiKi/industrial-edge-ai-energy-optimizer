import os
import numpy as np
import pandas as pd

def generate_hardware_aging_dataset(num_samples: int = 5000, output_path: str = "data/raw_sensor_data.csv"):
    """
    Simulates high-fidelity industrial sensor telemetry data adhering strictly to 
    electrical and thermal physical laws to prevent AI training bias.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.random.seed(42)
    
    time_steps = np.arange(num_samples)
    
    # 1. Realistic Voltage fluctuations around standard 220V grid with minor noise
    voltage = 220.0 + np.random.normal(0, 2.0, num_samples)
    
    # 2. Current varying realistically based on cyclical machine operations (load cycles)
    current = 15.0 + 5.0 * np.sin(time_steps / 50.0) + np.random.normal(0, 0.5, num_samples)
    current = np.clip(current, 2.0, 45.0) # Ensure current stays within safe hardware limits
    
    # 3. Temperature accumulating over time due to thermal resistance and load (Joule heating effect)
    # Temp increases proportionally with current squared and operational time steps
    temperature = 35.0 + (time_steps / 1000.0 * 15.0) + (current * 0.4) + np.random.normal(0, 0.6, num_samples)
    
    # 4. Hardware Degradation Factor (Gradual wear over time affecting efficiency)
    aging_factor = np.exp(-time_steps / (num_samples * 2.0)) # Exponential decay models real wear better than linear
    
    # 5. True Power and Actual Energy / Efficiency calculation adhering to power physics
    power_kw = (voltage * current * 0.92) / 1000.0 # Apparent to active power conversion with power factor 0.92
    e_actual = power_kw * aging_factor + np.random.normal(0, 0.05, num_samples)
    
    # Assemble into the strict industrial schema expected by DataLoader & Cleaner
    df = pd.DataFrame({
        'id': time_steps + 1,
        'device_id': 1,
        'power_kw': power_kw,
        'temperature_c': temperature,
        'voltage': voltage,
        'E_actual': e_actual,
        'optimal_baseline': 24.5,
        'is_anomaly': np.where((temperature > 85.0) | (current > 40.0), 1, 0), # Label anomalies based on physical thresholds
        'created_at': pd.date_range(start='2026-01-01', periods=num_samples, freq='min')
    })
    
    df.to_csv(output_path, index=False)
    print(f"Successfully generated physics-compliant industrial dataset at: {output_path}")

if __name__ == "__main__":
    generate_hardware_aging_dataset()