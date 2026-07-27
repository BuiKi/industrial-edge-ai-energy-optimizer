Dưới đây là file **`README.md`** dành riêng cho thư mục **`app/security`** mà bạn vừa yêu cầu:

````markdown
# 🔐 Security Module (`app/security`)

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.11.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-green.svg)
![Passlib](https://img.shields.io/badge/Passlib-Bcrypt-red.svg)
![JWT](https://img.shields.io/badge/Auth-JWT-orange.svg)

</div>

---

## 📌 Overview

The `security` module provides robust authentication, cryptographic hashing, JSON Web Token (JWT) management, and Role-Based Access Control (RBAC) dependency injections for the **Industrial Edge AI Energy Optimization Module**[cite: 13, 14, 15]. It guarantees secure credential handling and multi-tenant authorization across all system endpoints[cite: 13, 14, 15].

---

## 📂 File Structure & Components

```text
app/security/
├── __init__.py     # Package initializer
├── hashing.py      # Secure password hashing and verification using bcrypt[cite: 13]
├── jwt.py          # JWT access token generation and cryptographic validation[cite: 14]
└── permissions.py  # FastAPI security dependencies, OAuth2 bearer verification, and RBAC[cite: 15]
```
````

---

## 🔍 Detailed Module Breakdown

### 1. `hashing.py` — Password Security & Hashing

- **Framework:** `passlib` (`CryptContext` with `bcrypt` scheme).

- **Functions:**
- `Hash.bcrypt(password: str) -> str`: Hashes plain-text passwords into secure strings optimized for database storage.

- `Hash.verify(plain_password: str, hashed_password: str) -> bool`: Verifies whether an input password matches the stored database hash.

### 2. `jwt.py` — Token Generation & Validation

- **Framework:** `python-jose` (`jwt`, `JWTError`).

- **Functions:**
- `create_access_token(data: dict, expires_delta: timedelta | None) -> str`: Generates a signed JSON Web Token containing client payloads and customizable expiration periods (defaulting to system settings).

- `verify_access_token(token: str, credentials_exception)`: Decodes and validates incoming tokens using the application's secret key and algorithm, safely returning the payload dictionary.

### 3. `permissions.py` — Authentication Dependencies & RBAC

- **Framework:** FastAPI (`OAuth2PasswordBearer`, `Depends`, `HTTPException`).

- **Components:**
- `oauth2_scheme`: Configures the OAuth2 bearer token scheme pointing to the `/auth/login` authentication route.

- `get_current_client`: FastAPI dependency that extracts and validates the token, querying the asynchronous database to fetch the authenticated client instance.

- `verify_infrastructure_admin`: Role-based access control (RBAC) dependency verifying if the requester holds infrastructure administrator privileges (`role == "infrastructure_admin"`), restricting high-level management and maintenance endpoints.
