````markdown
# 🌐 API Routers Module (`app/routers`)

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.11.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-green.svg)
![WebSockets](https://img.shields.io/badge/Realtime-WebSockets-orange.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blueviolet.svg)

</div>

---

## 📌 Overview

The `routers` module contains the FastAPI endpoint definitions for the **Industrial Edge AI Energy Optimization Module**. It exposes structured, version-safe RESTful APIs and real-time WebSocket communication channels to handle client management, authentication, device tracking, sensor telemetry streaming, system alerts, and automated database maintenance.

---

## 📂 File Structure & Components

```text
app/routers/
├── __init__.py         # Package initializer
├── alerts.py           # System anomaly and alert management endpoints
├── auth.py             # Client credential authentication and JWT token generation
├── clients.py          # Tenant management and password update endpoints
├── devices.py          # Industrial hardware registration and state controls
├── maintenance.py      # Automated data pruning and retention cleanup endpoints
└── sensor_data.py      # High-frequency telemetry ingestion, batch saving, and WebSocket broadcasting
```
````

---

## 🔍 Detailed Module Breakdown

### 1. `alerts.py` — System Alert Management

- **Prefix:** `/alerts` | **Tags:** `Alerts`

- **Endpoints:**
- `POST /`: Creates a new system anomaly or energy deviation alert record.

- `GET /`: Retrieves a paginated list of system alerts.

### 2. `auth.py` — Authentication & Security

- **Prefix:** `/auth` | **Tags:** `Authentication`

- **Endpoints:**
- `POST /login`: Authenticates client credentials via `OAuth2PasswordRequestForm`, verifies password hashes, and returns a signed JSON Web Token (JWT) containing the client identifier in the payload.

### 3. `clients.py` — Tenant Management & Self-Service

- **Prefix:** `/clients` | **Tags:** `Clients Management`

- **Endpoints:**
- `POST /`: Registers a new client (restricted to Infrastructure Admins via dependency injection).

- `GET /`: Retrieves a paginated list of all active clients (admin-restricted).

- `DELETE /{client_id}/`: Performs a soft delete on a target client account.

- `PUT /{client_id}/restore/`: Restores a soft-deleted client back to active status.

- `PUT /change-password`: Allows an authenticated client to securely update their own password after validating current credentials.

### 4. `devices.py` — Hardware Unit Management

- **Prefix:** `/devices` | **Tags:** `Devices`

- **Endpoints:**
- `POST /`: Registers a new industrial hardware device linked to a client.

- `GET /`: Retrieves a paginated list of active devices.

- `DELETE /{device_id}/`: Soft-deletes a hardware device by ID.

- `PUT /{device_id}/restore/`: Restores a soft-deleted hardware unit.

### 5. `maintenance.py` — Database Cleanup & Retention

- **Prefix:** `/maintenance` | **Tags:** `Maintenance`

- **Endpoints:**
- `DELETE /purge-old-data/`: Executes automated data retention routines, permanently purging expired soft-deleted clients/devices (>30 days) and outdated sensor telemetry/alert history (>90 days).

### 6. `sensor_data.py` — Telemetry Ingestion & Real-Time WebSockets

- **Prefix:** `/sensor-data` | **Tags:** `Sensor Telemetry`

- **Core Feature (`ConnectionManager`):** Manages active WebSocket connections to broadcast live telemetry frames instantly to connected dashboard clients (such as Streamlit).

- **Endpoints:**
- `POST /`: Ingests a single high-frequency sensor reading, saves it to PostgreSQL, and triggers a real-time broadcast event (`NEW_SENSOR_DATA`).

- `POST /batch`: Ingests a batch of telemetry records to optimize hardware bandwidth and triggers a batch broadcast event (`NEW_BATCH_DATA`).

- `GET /`: Retrieves global paginated sensor readings.

- `GET /devices/{device_id}/sensor-data/`: Fetches historical telemetry specific to a target hardware device ID.

- `WEBSOCKET /ws`: Persistent bi-directional streaming endpoint for live dashboard telemetry updates.

---
