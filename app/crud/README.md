````markdown
# 🛠️ CRUD Operations Module (`app/crud`)

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.11.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-AsyncIO-red.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blueviolet.svg)

</div>

---

## 📌 Overview

The `crud` module implements the data access layer for the **Industrial Edge AI Energy Optimization Module**. It encapsulates all asynchronous database interaction logic (Create, Read, Update, Delete) using SQLAlchemy and Pydantic schemas, ensuring structured, secure, and high-performance operations across all business entities[cite: 5].

---

## 📂 File Structure & Components

```text
app/crud/
├── __init__.py     # Package initializer
└── crud.py         # Asynchronous data access queries for clients, devices, sensors, and alerts
```
````

---

## 🔍 Detailed Module Breakdown (`crud.py`)

### 1. Client Management (`Client CRUD`)

- **`get_client`**: Retrieves a single active client by unique database ID.

- **`get_clients`**: Fetches a paginated list of active clients.

- **`create_client`**: Registers a new client record, auto-generating a unique client identifier if needed and hashing passwords securely using bcrypt.

- **`soft_delete_client`**: Marks a client as inactive and logs the precise UTC timestamp of deletion.

- **`restore_client`**: Recovers a soft-deleted client back to active operational status.

- **`purge_old_deleted_clients`**: Permanently deletes client records that have exceeded the specified soft-delete retention threshold (default: 30 days).

- **`update_client_password`**: Validates the existing password, hashes the new password securely, and updates the client credentials.

### 2. Device Management (`Device CRUD`)

- **`get_device`**: Queries a single active hardware device by ID.

- **`get_devices`**: Retrieves a paginated list of active hardware devices.

- **`create_device`**: Links and registers a new industrial hardware unit to a specific client.

- **`soft_delete_device`**: Deactivates a device and records its deletion timestamp.

- **`restore_device`**: Restores a soft-deleted hardware device back to active state.

- **`purge_old_deleted_devices`**: Permanently cleans up devices soft-deleted beyond the designated retention timeline.

### 3. Sensor Telemetry & Data Management (`Sensor Data CRUD`)

- **`create_sensor_data`**: Persists a single real-time telemetry reading (power, temperature, voltage, optimal baseline, and anomaly flags).

- **`create_sensor_data_batch`**: Optimizes database throughput by inserting high-frequency sensor readings in structured batches.

- **`get_sensor_data_by_device`**: Queries historical telemetry logs for a target device with support for pagination.

- **`delete_old_sensor_data`**: Purges outdated sensor records exceeding the storage retention policy (default: 90 days) to optimize disk space.

### 4. System Alerts & Anomaly Management (`Alert CRUD`)

- **`create_alert`**: Logs a new system anomaly or energy deviation alert linked to a device.

- **`get_alerts`**: Fetches a paginated list of all system alerts.

- **`delete_old_alerts`**: Cleans up historical alert records older than the specified retention period.

---
