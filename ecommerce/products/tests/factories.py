import uuid

import factory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "products.Product"

    id = factory.LazyAttribute(lambda o: uuid.uuid4().hex)
    name = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
