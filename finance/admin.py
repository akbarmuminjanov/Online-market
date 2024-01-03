from django.contrib import admin
from .models import DebtArrivedCargo, DebtCustomer
# Register your models here.



admin.site.register([DebtArrivedCargo, DebtCustomer])