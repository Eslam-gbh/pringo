from django.test import TestCase
from nose.tools import eq_, ok_
from .factories import SKUFactory
from ..serializers import AvailableStoragesSerializer


class TestAvailableStoragesSerializerSerializer(TestCase):
    def setUp(self):
        self.sku1 = SKUFactory(id='abc')
        self.sku2 = SKUFactory(id='def')
        self.data = {
            'lines': [{
                'sku': 'abc',
                'quantity': 12
            }, {
                'sku': 'def',
                'quantity': 2
            }]
        }

    def test_serializer_with_empty_data(self):
        serializer = AvailableStoragesSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = AvailableStoragesSerializer(data=self.data)
        ok_(serializer.is_valid())

    def test_serializer_with_invalid_data(self):
        self.data['lines'][0]['sku'] = 'inavlid_sku'
        serializer = AvailableStoragesSerializer(data=self.data)
        eq_(serializer.is_valid(), False)

    def test_serializer_grouping_data(self):
        serializer = AvailableStoragesSerializer(data=self.data)
        ok_(serializer.is_valid())
        expected_result = {'abc': 12, 'def': 2}
        result = serializer.group_list_lines_into_sku_quantity_dict(self.data['lines'])
        self.assertDictEqual(result, expected_result)
