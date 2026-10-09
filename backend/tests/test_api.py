import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.main import app
from app.core.database import engine, Base, SessionLocal
from app.seed_data import seed_database

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

def test_health_check():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

def test_get_products():
    with TestClient(app) as client:
        response = client.get("/api/products")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1

def test_get_brand_kit():
    with TestClient(app) as client:
        response = client.get("/api/brand-kit")
        assert response.status_code == 200
        data = response.json()
        assert "primary_color" in data
        assert "name" in data

def test_get_analytics():
    with TestClient(app) as client:
        response = client.get("/api/analytics/overview")
        assert response.status_code == 200
        data = response.json()
        assert "total_campaigns" in data
        assert "average_qc_score" in data

def test_product_import_url():
    with TestClient(app) as client:
        response = client.post("/api/products/import-url", json={"url": "https://www.amazon.com/dp/B09ABCDEF"})
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert len(data["features"]) > 0
