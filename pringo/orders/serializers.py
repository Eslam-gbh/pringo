from collections import defaultdict
from rest_framework import serializers
from .models import Order, OrderLine, SKU, Storage


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        exclude = ('version', )


class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = ('sku', 'quantity', )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('customer_name_decoded', )


class AvailableStoragesSerializer(serializers.Serializer):
    lines = OrderLineSerializer(many=True)

    def group_list_lines_into_sku_quantity_dict(self, lines):
        lines_dict = defaultdict(lambda: 0)
        for line in lines:
            lines_dict[line['sku']] += line['quantity']
        return dict(lines_dict)
