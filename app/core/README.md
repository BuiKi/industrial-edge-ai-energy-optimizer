

````markdown
# ⚙️ Core Module (`app/core`)

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.11.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-AsyncIO-red.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blueviolet.svg)

</div>

---

## 📌 Overview

The `core` module serves as the architectural backbone of the **Industrial Edge AI Energy Optimization Module**. It centralizes system-wide configurations, manages secure environment variables, and establishes high-performance asynchronous database connections to support high-frequency industrial telemetry ingestion.

---

## 📂 File Structure & Components

```text
app/core/
├── __init__.py         # Package initializer
├── config.py           # Pydantic-based environment settings & security configs
├── database.py         # Asynchronous SQLAlchemy engine & session dependency
└── init_database.py    # Database schema auto-generator for PostgreSQL
```
````

---

## 🔍 Detailed Module Breakdown

### 1. `config.py` — Global Configuration & Environment Management

- **Framework:** `pydantic-settings` (`BaseSettings`, `SettingsConfigDict`).

- **Key Responsibilities:**
- Automatically loads and validates environment variables from the local `.env` file with `utf-8` encoding.

- Defines core system parameters including project identity (`PROJECT_NAME`), database connection strings (`DATABASE_URL`), and security credentials.
- Manages JSON Web Token (JWT) settings (`SECRET_KEY`, `ALGORITHM = "HS256"`, `ACCESS_TOKEN_EXPIRE_MINUTES = 30`).

- Exposes a centralized, pre-instantiated `settings` object imported across the entire application.

### 2. `database.py` — Asynchronous Database Engine & Session Provider

- **Framework:** SQLAlchemy (`AsyncIO`, `create_async_engine`, `sessionmaker`).

- **Key Responsibilities:**
- Initializes an asynchronous database engine (`async engine`) connected to PostgreSQL via the `postgresql+asyncpg://` driver.

- Configures `SessionLocal` as an `AsyncSession` factory to handle non-blocking database operations, maximizing throughput under heavy industrial loads.

- Implements the FastAPI Dependency Injection utility (`get_db`):
- Automatically provisions an active async session.
- Commits transactions upon successful request completion.
- Rolls back changes safely if an exception occurs.
- Guarantees proper resource cleanup by closing the session in a `finally` block.

### 3. `init_database.py` — Schema Initialization Script

- **Key Responsibilities:**
- Scans all registered ORM models (`Client`, `Device`, `SensorData`, `Alert`).

- Automatically provisions and creates the full multi-tenant schema (4 core tables) directly inside the PostgreSQL database if they do not already exist.

---
