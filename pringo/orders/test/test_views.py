import json
from django.urls import reverse
from nose.tools import eq_
from rest_framework.test import APITestCase
from rest_framework import status
from .factories import SKUFactory, StorageFactory, OrderFactory


class TestOrderTestCase(APITestCase):
    """
    Tests /order list operations.
    """
    @classmethod
    def setUpTestData(cls):
        sku1 = SKUFactory(id='abc')
        sku2 = SKUFactory(id='def')
        StorageFactory(id='zzz', sku=sku1, stock=5)
        StorageFactory(id='yyy', sku=sku1, stock=100)
        StorageFactory(id='xxx', sku=sku2, stock=100)
        cls.order = OrderFactory(customer_name='Thomas Müller')
        cls.data = {
            'lines': [{
                'sku': 'abc',
                'quantity': 12
            }, {
                'sku': 'def',
                'quantity': 2
            }]
        }
        cls.url = reverse('order-list') + 'available-storages/'

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(
            self.url,
            content_type='application/json',
            data=json.dumps(self.data),
        )
        eq_(response.status_code, status.HTTP_200_OK)

        expected_response = [{
            'id': 'zzz',
            'quantity': 5
        }, {
            'id': 'yyy',
            'quantity': 7
        }, {
            'id': 'xxx',
            'quantity': 2
        }]
        self.assertDictEqual({'storages': expected_response}, response.data)

    def test_filter_order(self):
        url = reverse('order-list') + '?q=muller'
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['count'], 1)
        eq_(response.data['results'][0]['customer_name'], 'Thomas Müller')

        url = reverse('order-list') + '?q=inavlid_name'
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['count'], 0)

    def test_duplicate_requests_fails(self):
        response = self.client.post(
            self.url,
            content_type='application/json',
            data=json.dumps(self.data),
            HTTP_X_IDEMPOTENCY_KEY='123',
        )
        eq_(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            self.url,
            content_type='application/json',
            data=json.dumps(self.data),
            HTTP_X_IDEMPOTENCY_KEY='123',
        )
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)
