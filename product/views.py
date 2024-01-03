from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import datetime
from .models import Product, ArrivedProduct, Customer, SelledProduct, Category
from .forms import ProductForm, CategoryForm, ArrivedCargoForm, ArrivedProductFormset, CustomerForm, SelledProductFormset
# Create your views here.


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return redirect("dashboard")
        
        return redirect("sell_product")

class ProductCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProductForm()
        return render(request, "create.html", {"form":form})
    
    def post(self, request):
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            form.save()
            messages.success(request, "Mahsulot muvafaqiyatli qoshildi")
            return redirect("list")
        else:
            return render(request, "create.html", {"form":form})

class ProductListView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all().select_related("category", "user")
        categories = Category.objects.all()

        context = {"products":products, "categories":categories}

        q = request.GET.get("q")
        category_id = request.GET.get("category")
        if q:
            products = Product.objects.filter(name__icontains=q)
            context['products'] = products
            context['q'] = q

        if category_id:
            # category = Category.objects.get(id=int(category_id))
            products = products.filter(category__id=int(category_id))
            context['products'] = products
            context['category_id'] = int(category_id)


        return render(request, "list.html", context)

class ProductDetailView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return HttpResponse(product.name)
       
class ProductUpdateView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, user=request.user)
        form = ProductForm(instance=product)
        return render(request, "update.html", {"form":form, "product":product})
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, user=request.user)
        form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Mahsulot muvafaqiyatli yangilandi")
            return redirect("list")
        else:
            return render(request, "update.html", {"form":form, "product":product})
    
class ProductDeleteView(LoginRequiredMixin, View):
    def get(self, request, product_id):
       product = get_object_or_404(Product, id=product_id, user=request.user) 
       return render(request, "delete.html", {"product":product})
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, user=request.user) 
        product_name = request.POST.get("product_name")
        if product_name == product.name:
            product.delete()
            messages.info(request, "Mahsulot muvafaqiyatli o'chirildi")
            return redirect("list")
        else:
            return HttpResponse("Error")
            # return render(redirect, "delete.html", {"product":product})
    
class ProductArrivedCargoView(LoginRequiredMixin, View):
    def get(self, request):
        form = ArrivedCargoForm()
        formset = ArrivedProductFormset()
        return render(request, "arrived_cargo.html", {"form":form, 'formset':formset})

    def post(self, request):
        form = ArrivedCargoForm(data=request.POST)
        if form.is_valid():
            arrivedcargo = form.save(commit=False)
            arrivedcargo.user = request.user
            # form.save()
            formset = ArrivedProductFormset(instance=arrivedcargo, data=request.POST)
            if formset.is_valid():
                form.save()
                formset.save()
                form.save()
                messages.success(request, "Mahsulot muvafaqiyatli sotib olindi")
                return redirect("list")
            
        return render(request, "arrived_cargo.html", {"form":form, 'formset':formset})
    
class ProductSellView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomerForm()
        formset = SelledProductFormset()
        return render(request, "sell_product.html", {"form":form, "formset":formset})
    
    def post(self, request):
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            # form.save()
            formset = SelledProductFormset(instance=customer, data=request.POST)
            if formset.is_valid():
                form.save()
                formset.save()
                form.save()
                messages.success(request, "Mahsulot muvafaqiyatli sotildi")
                return redirect('customer_detail', customer.id)

        return render(request, "sell_product.html", {"form":form, "formset":formset})
    
class CuctomerDetail(LoginRequiredMixin, View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        return render(request, "customer_detail.html", {"customer":customer})
    
class TodaysSellsView(LoginRequiredMixin, View):
    def get(self, request):
        today = datetime.today()
        customers = Customer.objects.filter(datetime__year=today.year, datetime__month=today.month, datetime__day=today.day, user=request.user).select_related("user")
        return render(request, "customer_list.html", {"customers":customers, "title":"Bugungi savdoindgiz"})