import logging
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SKU, OrderLine, Storage, Order
from .utils import unidecode_string
from .serializers import (
    OrderSerializer,
    SKUSerializer,
    OrderLineSerializer,
    StorageSerializer,
    AvailableStoragesSerializer,
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

    def get_queryset(self):
        customer_name = self.request.query_params.get('q', None)
        if customer_name:
            return Order.objects.filter(customer_name_decoded__icontains=unidecode_string(customer_name))
        else:
            return super().get_queryset()

    @action(detail=False,
            methods=['post'],
            url_path='available-storages',
            url_name='available_storages')
    def available_storages(self, request, pk=None):
        try:
            serializer = AvailableStoragesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            lines_dict = serializer.group_list_lines_into_sku_quantity_dict(request.data['lines'])
            storages = Storage.objects.get_available_storages(lines_dict)
            return Response({'storages': storages})
        except (AssertionError, ValidationError) as e:
            logger.exception(
                f'Error: {e} happened while getting available_storages for data {request.data}'
            )
            return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
