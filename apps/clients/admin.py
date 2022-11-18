from django.contrib import admin
from apps.clients.models import Client, Budget #, Purchase

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    pass


# @admin.register(Purchase)
# class PurchaseAdmin(admin.ModelAdmin):
#     pass