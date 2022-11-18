import datetime
from pyexpat import model
import keepa
import ast

from core.settings import KEEPA_KEY
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save, pre_save

from apps.products.utils import format_json_keepa

class Product(models.Model):
    """ Model of a product """
    asin = models.CharField(max_length=10, unique=True)
    brand = models.CharField(max_length=255)
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    last_price_buy_box = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    json_keepa = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    @property
    def url_image(self):
        if self.image:
            return "https://m.media-amazon.com/images/I/{}".format(self.image)
        return self.image

    @property
    def url_amazon(self):
        if self.image:
            return "https://www.amazon.com/dp/{}/".format(self.asin)
        return self.image

    def get_data_keepa(self):
        try:
            api = keepa.Keepa(KEEPA_KEY)
            product = api.query(self.asin, progress_bar=False, domain='US')

            # If not data in csv means that no information of that product in that region
            if all(element == None for element in product[0]['csv']):
                return False, Exception('There is not information of this ASIN in USA')

            return True, format_json_keepa(product[0])
        except Exception as exc:
            return False, exc

    def json_keepa_to_dict(self):
        """Method to get json_keepa property as a dict"""
        return ast.literal_eval(self.json_keepa)
    
    def store_product_data(self):
        """Method for storing remaining product data."""
        succes, json_keepa = self.get_data_keepa()
        if succes:
            self.json_keepa = json_keepa
            self.title = json_keepa['title']
            self.brand = json_keepa['brand']
            self.description = json_keepa['description']
            self.size = json_keepa['size']
            self.color = json_keepa['color']
            self.image = json_keepa['imagesCSV'].split(',')[0]
            self.last_price_buy_box = json_keepa['data']['NEW'][-1]
            self.save()
        else:
            raise Exception("Failed to get product information in keepa. Check if the ASIN code is correct. {}".format(self.asin))

    def is_available(self):
        """Method to know if the product is available. Took 30 days to the last request approved"""
        now = timezone.now()
        date = now - datetime.timedelta(days=30)
        if self.products_entries.filter(status__in=('approved','pending'), created_at__lte=now, created_at__gte=date).exists():
            return False
        return True

@receiver(post_save, sender=Product)
def product_post_save_receiver(sender, instance, **kwargs):
    product = instance
    ProductHistory.objects.create(
        product=product,
        title=product.title,
        description=product.description,
        brand=product.brand,
        size=product.size,
        color=product.color,
        amount=product.last_price_buy_box,
        json_keepa=product.json_keepa
    )


class ProductHistory(models.Model):
    product = models.ForeignKey(
        Product, related_name="history", on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    brand = models.TextField()
    size = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    json_keepa = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product History'
        verbose_name_plural = 'Products Histories'


class ProductEntry(models.Model):
    """ Model of a Product Entry """

    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    product = models.ForeignKey(Product, related_name="products_entries", null=True, on_delete=models.CASCADE)
    searcher = models.ForeignKey('authentication.User', related_name="searchers", null=True, on_delete=models.SET_NULL)
    supervisor = models.ForeignKey('authentication.User', related_name="supervisors", null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey('clients.Client', related_name="products_entries", null=True, on_delete=models.CASCADE)
    # account_manager = models.Fe
    folio = models.CharField(max_length=10)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='pending')
    store = models.CharField(max_length=255)
    link_store = models.URLField(max_length=200)
    buy_amount_per_piece = models.DecimalField(max_digits=12, decimal_places=2)
    observations = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason_rejection = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Entry"
        verbose_name_plural = "Products Entries"
        permissions = (("can_approve", "Set product as approved"),)


    def __str__(self):
        return self.folio

    def generate_folio(self):
        last_request = ProductEntry.objects.last()
        if last_request:
            num = int(last_request.folio) + 1
        else:
            num = 1
        num = str(num)

        return "{}{}".format('0'*(8-len(num)), num)

    def get_budgets_availables(self):
        """Method to know how many budgets are availables yet"""
        quantity = self.quantity
        budgets = self.budgets.all()
        if budgets:
            for budget in budgets:
                quantity -= budget.quantity

        return quantity

@receiver(pre_save, sender=ProductEntry)
def generate_folio(sender, instance, **kwargs):
    if not instance.folio:
        instance.folio = instance.generate_folio()
