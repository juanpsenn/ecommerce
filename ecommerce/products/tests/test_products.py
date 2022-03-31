from .factories import ProductFactory


def test_get_all_products(api_client):
    ProductFactory.create_batch(3)
    response = api_client.get("/products/")
    assert response.status_code == 200
    assert len(response.data) == 3


def test_get_product_by_id(api_client):
    product = ProductFactory()
    response = api_client.get(f"/products/{product.id}/")
    assert response.status_code == 200
    assert response.data["id"] == product.id


def test_get_non_existing_product(api_client):
    response = api_client.get("/products/12345/")
    assert response.status_code == 404


def test_post_product(api_client):
    body = {"id": "not-an-id", "name": "some-random-name", "price": 1.0}
    response = api_client.post("/products/", data=body, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "some-random-name"
    assert float(response.data["price"]) == 1.00


def test_post_product_with_invalid_id(api_client):
    body = {"id": "not-an-id", "price": 1.0}
    response = api_client.post("/products/", data=body, format="json")
    assert response.status_code == 400


def test_put_product(api_client):
    product = ProductFactory()
    body = {"id": product.id, "name": "some-random-name", "price": 1.0}
    response = api_client.put(f"/products/{product.id}/", data=body, format="json")
    assert response.status_code == 200
    assert response.data["name"] == "some-random-name"
    assert float(response.data["price"]) == 1.00


def test_update_product_stock(api_client):
    product = ProductFactory(stock=10)
    body = {"stock": 20}
    response = api_client.put(
        f"/products/{product.id}/stock-update/", data=body, format="json"
    )

    product.refresh_from_db()

    assert response.status_code == 200
    assert response.data["stock"] == 20
    assert product.stock == 20
