from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)
        self.assertEqual(first=response.context_data['title'], second='Parfenovka Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self) -> None:
        self.products = Product.objects.all()

    def _common_tests(self, response) -> None:
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(first=response.context_data['title'], second='Parfenovka Store | Каталог')

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            first=list(response.context_data['object_list']),
            second=list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            first=list(response.context_data['object_list']),
            second=list(self.products.filter(category_id=category.id)[:3]))

    # def test_last_page_list(self):
    #     goods_count = self.products.count()
    #     last_page = goods_count // 3 if goods_count % 3 == 0 else goods_count // 3 + 1
    #     path = reverse('products:paginator', kwargs={'page': last_page})
    #     response = self.client.get(path)
    #
    #     self._common_tests(response)
    #     self.assertEqual(
    #         first=list(response.context_data['page_obj'][:-1]),
    #         second=list(self.products.all()[:3]))
