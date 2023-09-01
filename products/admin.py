from django.contrib import admin

from products.models import Basket, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # отображение объектов в таблице
    list_display = ('name', 'price', 'quantity', 'category')
    # отображение выбранного объекта
    fields = ('name', 'description',
              ('price', 'quantity'),
              'image', 'category',
              'stripe_product_price_id')  # кортеж внутри кортежа позволяет поместить поля в одну строку
    readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('-name',)  # сортировка в обратном алфавитном порядке


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0  # вывод дополнительных пустых полей для заполнения новой корзины
