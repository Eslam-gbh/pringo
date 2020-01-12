from django.db import models
from ool import VersionField, VersionedMixin


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OptimisticConcurrencyBaseModel(VersionedMixin, BaseModel):
    version = VersionField()

    class Meta:
        abstract = True


class Order(BaseModel):
    customer_name = models.CharField(
        max_length=50
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f'Order for customer {self.customer_name}'


class OrderLine(OptimisticConcurrencyBaseModel):
    class Meta:
        verbose_name = "Order Line"
        verbose_name_plural = "Order Lines"

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
    )

    sku = models.ForeignKey(
        'SKU',
        on_delete=models.SET_NULL,
        null=True,
    )

    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Order Line for order {self.order_id} and SKU {self.sku_id} with quantity {self.quantity}"


class Storage(OptimisticConcurrencyBaseModel):
    class Meta:
        verbose_name = "Storage"
        verbose_name_plural = "Storages"

    id = models.CharField(max_length=100, primary_key=True)
    stock = models.PositiveSmallIntegerField()
    sku = models.ForeignKey(
        'SKU',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Storage {self.id} for SKU {self.sku_id} with quantity {self.stock}"


class SKU(BaseModel):
    class Meta:
        verbose_name = "SKU"
        verbose_name_plural = "SKUs"

    product_name = models.CharField(max_length=250)

    def __str__(self):
        return f"SKU {self.product_name}"
