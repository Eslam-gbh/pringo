import logging

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
# from django_filters.rest_framework import DjangoFilterBackend

from .models import SKU, OrderLine, Storage, Order
from .serializers import (
    OrderSerializer,
    SKUSerializer,
    OrderLineSerializer,
    StorageSerializer,
)

logging.basicConfig()
logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Updates and retrieves Orders
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny, )


class SKUViewSet(viewsets.ModelViewSet):
    """
    Updates and retrieves SKUs
    """
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer
    permission_classes = (AllowAny, )


class OrderLineViewSet(viewsets.ModelViewSet):
    """
    Updates and retrieves OrderLines
    """
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer
    permission_classes = (AllowAny, )


class StorageViewSet(viewsets.ModelViewSet):
    """
    Updates and retrieves Storages
    """
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = (AllowAny, )
