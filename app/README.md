````markdown
# 🚀 FastAPI Application Core (`app/`)

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.11.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-AsyncIO-red.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blueviolet.svg)
![WebSockets](https://img.shields.io/badge/Realtime-WebSockets-orange.svg)

</div>

---

## 📌 Overview

The `app` directory contains the complete backend application architecture for the **Industrial Edge AI Energy Optimization Module**. Built on top of **FastAPI** and **SQLAlchemy (AsyncIO)**, it is engineered to handle high-frequency industrial telemetry ingestion, real-time WebSocket broadcasting, secure multi-tenant client management, automated anomaly alerts, and database maintenance routines.

---

## 📂 Directory Structure

```text
app/
├── core/           # System configurations, async database engine, and schema initializers
├── crud/           # Asynchronous data access layer (Clients, Devices, Sensors, Alerts)
├── models/         # SQLAlchemy ORM relational database models
├── routers/        # RESTful API endpoints and WebSocket communication streams
├── schemas/        # Pydantic v2 validation and serialization models
└── security/       # Authentication, JWT tokens, password hashing, and role permissions
```
````

---

## 🧩 Module Breakdown

### 1. `core/` — Configuration & Database Engine

- Manages environment variables securely using `pydantic-settings`.
- Establishes non-blocking asynchronous PostgreSQL connections via `asyncpg` and SQLAlchemy.
- Provides session dependency injection (`get_db`) for all application endpoints.

### 2. `crud/` — Data Access Layer

- Implements structured asynchronous database queries for all core entities.
- Supports single and batch telemetry inserts, soft deletion logic, account restoration, and automated record purging.

### 3. `models/` — Relational ORM Models

- Defines multi-tenant database tables: `clients`, `device`, `sensor_data`, and `alerts`.
- Integrates performance optimizations such as composite indexing (`idx_device_created_at`) for high-speed time-series queries.

### 4. `routers/` — API Endpoints & Real-Time Streams

- **`/auth`**: Client authentication and secure JWT access token generation.
- **`/clients`**: Tenant management and self-service credential updates.
- **`/devices`**: Industrial hardware registration and operational state tracking.
- **`/sensor-data`**: High-frequency telemetry ingestion (single/batch) and bi-directional WebSocket broadcasting (`/ws`).
- **`/alerts`**: System anomaly detection and deviation logging.
- **`/maintenance`**: Automated database retention cleanup routines.

### 5. `schemas/` — Pydantic Validation Models

- Ensures type-safe validation and serialization for incoming payloads and outgoing database responses using Pydantic v2.

### 6. `security/` — Authentication & Permissions

- Handles bcrypt password hashing, JWT creation/verification, and role-based access control (RBAC) via dependency injection.

---
