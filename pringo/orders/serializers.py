# from rest_framework import exceptions
from rest_framework import serializers
from .models import Order, OrderLine, SKU, Storage
# from pizzai.users.serializers import UserSerializer
# from django.db import transaction
# from django.conf import settings


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'
        exclude = ('version', )


class OrderLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderLine
        fields = '__all__'
        exclude = ('version', )


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
