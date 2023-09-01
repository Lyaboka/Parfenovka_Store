from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import CommonContextMixin
from products.models import Basket, Product, ProductCategory

# from django.core.cache import cache


class IndexView(CommonContextMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Parfenovka Store'


class ProductsListView(CommonContextMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Parfenovka Store | Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        # categories = cache.get('categories')  # включить в продакшене и удалить следующую строку
        categories = ProductCategory.objects.all()
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            # cache.set('categories', context['categories'], 30)  # включить в продакшене
        else:
            context['categories'] = categories
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset


class BasketListView(CommonContextMixin, TemplateView):
    template_name = 'products/baskets.html'
    title = 'Parfenovka Store | Корзина'


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
