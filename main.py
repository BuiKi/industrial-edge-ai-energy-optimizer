from fastapi import FastAPI
from app.routers import auth, alerts, clients, devices, maintenance, telemetry

app = FastAPI(title="Industrial Edge AI System")

# Đăng ký các router con vào ứng dụng chính
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(devices.router)
app.include_router(telemetry.router)
app.include_router(alerts.router)
app.include_router(maintenance.router)