import uuid

import factory


class OrderDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "orders.OrderDetail"

    product = factory.SubFactory("products.tests.factories.ProductFactory", stock=10)
    quantity = 1


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "orders.Order"

    id = factory.LazyAttribute(lambda o: uuid.uuid4().hex)

    @factory.post_generation
    def create_details(self, create, extracted, **kwargs):
        if not create:
            return
        return OrderDetailFactory.create(order=self)
