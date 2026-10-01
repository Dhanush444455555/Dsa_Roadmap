import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Problem, CheatSheet

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_register_and_login():
    import time
    # Register test user
    email = f"test_user_phase2_{int(time.time()*1000)}@example.com"
    pwd = "password123"
    reg_resp = client.post("/api/auth/register", json={
        "email": email,
        "password": pwd,
        "name": "Test Engineer"
    })
    assert reg_resp.status_code == 200
    data = reg_resp.json()
    assert "access_token" in data
    assert data["user"]["email"] == email

    # Login
    login_resp = client.post("/api/auth/login", json={
        "email": email,
        "password": pwd
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    token = login_data["access_token"]
    assert token is not None

    # Get /me
    me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == email

    # Update settings
    settings_resp = client.put("/api/auth/settings", json={
        "timezone": "Asia/Kolkata",
        "reminder_time": "08:30",
        "duration_months": 6,
        "level": "Average",
        "daily_count": 2
    }, headers={"Authorization": f"Bearer {token}"})
    assert settings_resp.status_code == 200
    assert settings_resp.json()["timezone"] == "Asia/Kolkata"
    assert settings_resp.json()["daily_count"] == 2
