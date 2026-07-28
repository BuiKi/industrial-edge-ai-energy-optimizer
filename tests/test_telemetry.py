import pytest

@pytest.mark.asyncio
async def test_create_sensor_data(async_client):
    """Kiểm tra API nhận một bản ghi cảm biến đơn lẻ."""
    payload = {
        "device_id": 1,
        "power_kw": 45.5,
        "temperature_c": 75.2,
        "voltage": 380.0,
        "optimal_baseline": 40.0,
        "is_anomaly": False
    }
    
    # Gửi request POST giả lập vào endpoint /sensor-data/
    response = await async_client.post("/sensor-data/", json=payload)
    
    # Kiểm tra mã trạng thái trả về (201 Created)
    assert response.status_code == 201
    data = response.json()
    assert data["device_id"] == 1
    assert data["power_kw"] == 45.5
    assert data["is_anomaly"] is False


@pytest.mark.asyncio
async def test_create_sensor_data_batch(async_client):
    """Kiểm tra API nhận dữ liệu cảm biến hàng loạt (Batch Ingestion)."""
    batch_payload = {
        "readings": [
            {
                "device_id": 1,
                "power_kw": 50.0,
                "temperature_c": 78.0,
                "voltage": 380.0,
                "optimal_baseline": 42.0,
                "is_anomaly": True
            },
            {
                "device_id": 1,
                "power_kw": 48.0,
                "temperature_c": 76.5,
                "voltage": 380.0,
                "optimal_baseline": 41.5,
                "is_anomaly": False
            }
        ]
    }
    
    # Gửi request POST giả lập vào endpoint /sensor-data/batch
    response = await async_client.post("/sensor-data/batch", json=batch_payload)
    
    # Kiểm tra kết quả trả về
    assert response.status_code == 201
    data = response.json()
    assert len(data) == 2
    assert data[0]["is_anomaly"] is True
    assert data[1]["power_kw"] == 48.0