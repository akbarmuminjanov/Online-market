from django.db import models
from users.models import User
# Create your models here.

MEASUREMENT_CHOISES = (
    ("kg", "Kilogram"),
    ("metr", "Metr"),
    ("pc", "Dona"),
    ("litr", "Litr"),
)

TYPE_OF_TRADE_CHOICES = (
    ("debt","Nasiya"),
    ("cash","Naqt"),
)

TYPE_OF_PRICE = (
    ("selling", "Sotilish Narxi"),
    ("wholesale", "Optom Narx"),
    ("actual", "Haqiqiy Narxi")
)

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
        
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    actual_price = models.PositiveBigIntegerField(help_text="Mahsulotni olib kelingan narxi")
    selling_price = models.PositiveBigIntegerField(help_text="Mahsulotni sotilish narxi")
    wholesale_price = models.PositiveBigIntegerField(help_text="Mahsulotni chakana narxi")
    type_of_measurement = models.CharField(max_length=5, choices=MEASUREMENT_CHOISES)
    quantity = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}, {self.quantity}, {self.type_of_measurement} qolgan" 

class ArrivedCargo(models.Model):
    supplier = models.CharField(max_length=150, verbose_name="Yetkazib beruvchi")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    type_of_trade = models.CharField(max_length=50, choices=TYPE_OF_TRADE_CHOICES, verbose_name="Savdo Turi")
    amount = models.PositiveBigIntegerField(default=0)

    
    def __str__(self):
        return str(self.supplier)
    
class ArrivedProduct(models.Model):
    cargo = models.ForeignKey(ArrivedCargo, on_delete=models.CASCADE, related_name="arrived_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return str(self.product.name)
    
class Customer(models.Model):
    name = models.CharField(max_length=150, verbose_name="Mijoz", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveBigIntegerField(default=0)
    type_of_trade = models.CharField(max_length=50, choices=TYPE_OF_TRADE_CHOICES, verbose_name="Savdo Turi")
    
    def __str__(self):
        return str(self.name)
    
class SelledProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    quantity = models.PositiveIntegerField(verbose_name="Miqdor")
    type_of_price = models.CharField(max_length=25, choices=TYPE_OF_PRICE, verbose_name="Narx turi")
    
    def __str__(self):
        return str(self.product.name)
    