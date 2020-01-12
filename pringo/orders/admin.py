from django.contrib import admin
from pringo.orders.models import Order, OrderLine, SKU, Storage

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(SKU)
admin.site.register(Storage)
