from django.contrib import admin
from apps.products.models import Product, ProductHistory, ProductEntry


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductHistory)
class ProductHistoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductEntry)
class ProductEntryAdmin(admin.ModelAdmin):
    pass
