from django.db import models
from users.models import User
from product.models import Product, ArrivedCargo, ArrivedProduct, Customer
from django.utils import timezone
# Create your models here.


class DebtArrivedCargo(models.Model):
    cargo = models.OneToOneField(ArrivedCargo, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payed_amount = models.PositiveBigIntegerField(default=0)
    
    @property
    def is_payed(self):
        return True if self.amount == 0 else False
    
    @property
    def is_late(self):
        return True if  timezone.now() - self.created > timezone.timedelta(days=31) else False 
    
    def __str__(self):
        return str(self.amount)
    
    class Meta:
        ordering = ["-created"]
    
class DebtCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payed_amount = models.PositiveBigIntegerField(default=0)
    
    @property
    def is_payed(self):
        return True if self.amount == 0 else False
    
    @property
    def is_late(self):
        return True if  timezone.now() - self.created > timezone.timedelta(days=31) else False 
    
    class Meta:
        ordering = ["-created"]