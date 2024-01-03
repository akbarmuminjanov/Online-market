from .models import Product, Category, ArrivedCargo, ArrivedProduct, Customer, SelledProduct
from django.forms import ModelForm, inlineformset_factory


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "image",
            "actual_price",
            "selling_price",
            "wholesale_price",
            "type_of_measurement",
        ]
        
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        
        
        
class ArrivedCargoForm(ModelForm):
    class Meta:
        model = ArrivedCargo
        fields = ["supplier", "type_of_trade"]
        

class ArrivedProductForm(ModelForm):
    class Meta:
        model =  ArrivedProduct
        fields = ["product", "quantity"]
        
        
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', "type_of_trade"]
        

class SelledProductForm(ModelForm):
    class Meta:
        model = SelledProduct
        fields = ["product", "quantity", "type_of_price"]

SelledProductFormset = inlineformset_factory(Customer, SelledProduct, form=SelledProductForm, fields=["product", "quantity", "type_of_price"],     extra=7, can_delete=False)
ArrivedProductFormset = inlineformset_factory(ArrivedCargo, ArrivedProduct, form=ArrivedProductForm, fields=["product", "quantity"],     extra=7, can_delete=False)