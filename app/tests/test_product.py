from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_product():
    # First create a category
    category_data = {"name": "Beverages", "description": "Drinks", "is_active": True}
    cat_response = client.post("/categories", json=category_data)
    assert cat_response.status_code == 201
    category_id = cat_response.json()["category_id"]

    product_data = {
        "sku": "COKE-001",
        "name": "Coca Cola",
        "description": "Soft drink",
        "unit_price": "1.50",
        "cost_price": "0.75",
        "quantity_in_stock": 100,
        "reorder_level": 10,
        "category_id": category_id,
        "supplier_id": None,
        "is_active": True,
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    assert response.json()["name"] == product_data["name"]
    assert response.json()["sku"] == product_data["sku"]
    assert response.json()["category_id"] == category_id