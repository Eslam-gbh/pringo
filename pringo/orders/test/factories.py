import factory


class SKUFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.SKU'

    id = factory.Faker('pystr', min_chars=1, max_chars=100)
    product_name = factory.Faker('pystr', min_chars=1, max_chars=250)


class StorageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.Storage'

    id = factory.Faker('pystr', min_chars=1, max_chars=100)
    sku = factory.SubFactory(SKUFactory)
    stock = factory.Faker('pyint')


class OrderLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.OrderLine'

    sku = factory.SubFactory(SKUFactory)
    quantity = factory.Faker('pyint')


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'orders.Order'

    customer_name = factory.Faker('name')
