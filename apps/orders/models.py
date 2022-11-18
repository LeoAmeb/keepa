from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator


class Order(models.Model):
    """Order's Model"""    
    product_entry = models.ForeignKey("products.ProductEntry", related_name="orders", on_delete=models.CASCADE)
    folio = models.CharField(max_length=10)
    store = models.CharField(max_length=255)
    link_store = models.URLField(max_length=200)
    buy_amount_per_piece = models.DecimalField(max_digits=12, decimal_places=2)
    observations = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_by = models.ForeignKey("authentication.User", related_name="orders_created", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_folio(self):
        last_request = Order.objects.last()
        if last_request:
            num = int(last_request.folio) + 1
        else:
            num = 1
        num = str(num)

        return "{}{}".format('0'*(8-len(num)), num)

    def __str__(self):
        return self.product_entry.product.title
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

@receiver(pre_save, sender=Order)
def generate_folio(sender, instance, **kwargs):
    if not instance.folio:
        instance.folio = instance.generate_folio()
