from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db import models
from apps.authentication.models import User


class Client(models.Model):
    """Model of Client"""
    user = models.OneToOneField(User, related_name="client", null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="clients_created", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Nombre del cliente
    # Configurar reembolsos
    # Agregar budget desde administrador -> supervisor para arriba
    # Orden de requests desc
    # Filtro mensual


    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
    
    def __str__(self):
        return self.user.get_full_name()


class Budget(models.Model):
    """Model of Budget"""
    BUDGETS_TYPES_CHOICES = [
        ('entry', 'Entry'),
        ('egress', 'Egress'),
    ]

    client = models.ForeignKey(Client, related_name="budgets", null=True, blank=True, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_by = models.ForeignKey(User, related_name="budgets_created", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        return "{} - {}".format(self.type, self.amount)


# class Purchase(models.Model):
#     client = models.ForeignKey(Client, related_name="purchases", on_delete=models.CASCADE)
#     budget = models.ForeignKey(Budget, related_name="purchases", on_delete=models.CASCADE)
#     order = models.ForeignKey("orders.Order", related_name="purchases", on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     quantity = models.IntegerField()
#     confirm = models.BooleanField(default=False)
#     user_created = models.ForeignKey(User, related_name="purchases", blank=True, null=True, on_delete=models.SET_NULL)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = 'Purchase'
#         verbose_name_plural = 'Purchases'
    
#     def __str__(self):
#         return "Order: {} - Budget: {} - Amount: {} ".format(self.order.folio, self.budget.amount, self.amount)    
    
# @receiver(pre_save, sender=Purchase)
# def rest_budget(sender, instance, **kwargs):
#     if instance.id is None:
#         instance.budget.amount -= instance.amount
#         instance.budget.save()
#     else:
#         previous = Purchase.objects.get(pk=instance.pk)
#         instance.budget.amount += previous.amount
#         instance.budget.amount -= instance.amount
#         instance.budget.save()

# @receiver(post_delete, sender=Purchase)
# def sum_budget(sender, instance, **kwargs):
#     """ Función para restar a lo condonado del gasto de cobranza """
#     instance.budget.amount += instance.amount
#     instance.budget.save()
