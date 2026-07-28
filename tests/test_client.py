import uuid
import pytest

@pytest.mark.asyncio
async def test_create_client(authenticated_client):
    """Kiểm tra API tạo mới một Client."""
    unique_suffix = uuid.uuid4().hex[:6]
    payload = {
        "company_name": f"Industrial Corp Test {unique_suffix}",
        "contact_email": f"contact_{unique_suffix}@industrial.com"
    }
    response = await authenticated_client.post("/clients/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == payload["company_name"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_clients(authenticated_client):
    """Kiểm tra API lấy danh sách Client."""
    response = await authenticated_client.get("/clients/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0