from django.urls import path

from .views import (CanceledTemplateView, OrderCreateView, OrderDetailView,
                    OrderListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='create'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('order-success/', SuccessTemplateView.as_view(), name='success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='canceled'),
]