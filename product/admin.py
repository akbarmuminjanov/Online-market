from django.contrib import admin
from .models import Category, Product, ArrivedCargo, ArrivedProduct, Customer, SelledProduct
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['name', "quantity", "type_of_measurement", "selling_price", 'actual_price', "wholesale_price", "created_at", "updated_at", ]
    search_fields = ["name"]
    list_filter = ['category']
    
    
admin.site.register([Category, ArrivedProduct, ArrivedCargo, SelledProduct, Customer])