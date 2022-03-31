from orders.models import Order
from products.tests.factories import ProductFactory

from .factories import OrderFactory


def test_get_all_orders(api_client):
    OrderFactory.create_batch(3)
    response = api_client.get("/orders/")
    assert response.status_code == 200
    assert len(response.data) == 3


def test_get_order_by_id(api_client):
    order = OrderFactory()
    product = order.items.first().product

    response = api_client.get(f"/orders/{order.id}/")
    assert response.status_code == 200
    assert response.data["id"] == order.id
    assert response.data["total"] == product.price


def test_get_non_existing_order(api_client):
    response = api_client.get("/orders/12345/")
    assert response.status_code == 404


def test_post_order(api_client):
    product = ProductFactory(id="abc", stock=10)
    body = {"id": "some-random-id", "items": [{"product": "abc", "quantity": 1}]}

    response = api_client.post("/orders/", data=body, format="json")

    product.refresh_from_db()

    assert response.status_code == 201
    assert response.data["id"] == "some-random-id"
    assert len(response.data["items"]) == 1
    assert product.stock == 9


def test_post_order_with_invalid_product(api_client):
    body = {"id": "some-random-id", "items": [{"product": "abc", "quantity": 1}]}

    response = api_client.post("/orders/", data=body, format="json")

    assert response.status_code == 400


def test_put_order(api_client):
    order = OrderFactory()
    product = order.items.first().product
    body = {"id": order.id, "items": [{"product": product.id, "quantity": 2}]}

    response = api_client.put(f"/orders/{order.id}/", data=body, format="json")

    product.refresh_from_db()

    assert response.status_code == 200
    assert response.data["id"] == order.id
    assert len(response.data["items"]) == 1
    assert product.stock == 9


def test_delete_order(api_client):
    order = OrderFactory()
    product = order.items.first().product
    response = api_client.delete(f"/orders/{order.id}/")

    product.refresh_from_db()

    assert response.status_code == 200
    assert Order.objects.count() == 0
    assert product.stock == 11  # Default stock value is 10
