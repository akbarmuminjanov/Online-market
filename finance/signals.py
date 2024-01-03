from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from product.models import ArrivedCargo, Customer
from django.db.models import Sum
from .models import DebtArrivedCargo, DebtCustomer



@receiver(pre_save, sender=ArrivedCargo)
def calculate_arrived_cargo(instance, *args, **kwargs):
    
        try:        
            arrived_products = instance.arrived_products.all()
            amount = 0
            for i in arrived_products:
                price = i.product.actual_price
                quantity = i.quantity
                amount += (price*quantity)
                
                
            instance.amount = amount

        except:
             pass

receiver(post_save, sender=ArrivedCargo)
def check_arrived_cargo_payment(instance, *args, **kwargs):
    if instance.type_of_trade == "debt":    
        debt, created =   DebtArrivedCargo.objects.get_or_create(cargo=instance, user=instance.user)
        debt.amount = instance.amount
        debt.save()      
            
@receiver(pre_save, sender=Customer)   
def calculate_customer_amount(instance, *args, **kwargs):

    try:
        selled_products = instance.selledproduct_set.all()
        amount = 0
        for i in selled_products:
            if i.type_of_price == 'selling':
                price = i.product.selling_price
            elif i.type_of_price == "actual":
                price = i.product.actual_price
            else:
                price = i.product.wholesale_price
                
            quantity = i.quantity    
            amount += (price*quantity)    

        instance.amount = amount
    except:
        print("No more")
        
@receiver(post_save, sender=Customer)   
def check_payment_type_customer(instance, *args, **kwargs):
    if instance.type_of_trade == "debt":    
        debt, created =   DebtCustomer.objects.get_or_create(customer=instance, user=instance.user)
        debt.amount = instance.amount
        debt.save()  