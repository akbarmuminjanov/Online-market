import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DebtArrivedCargo, DebtCustomer
from .mixins import AdminRequiredMixin
from product.models import ArrivedCargo, Customer
from django.contrib import messages
from django.utils.timezone import datetime, timedelta
from django.db.models import Sum

# Create your views here.


class DebtArrivedCargoListView(AdminRequiredMixin, View):
    def get(self, request):
        debts = DebtArrivedCargo.objects.all().select_related("cargo", "user", "cargo__user").prefetch_related("cargo__arrived_products")
        
        return render(request, "debt_arrived_cargo.html", {"debts":debts})

    def post(self, request):
        debt_id = request.POST.get("debt_id")
        amount = request.POST.get("amount")
        if debt_id and amount:
            debt = DebtArrivedCargo.objects.get(id=int(debt_id))
            debt.amount -= int(amount)
            debt.payed_amount += int(amount)
            debt.save()
            return redirect("debt_arrived_cargo_list")

class DebtCustomerListView(AdminRequiredMixin, View):
    def get(self, request):
        debts = DebtCustomer.objects.all().select_related("customer", "user").prefetch_related("customer__selledproduct_set", "customer__selledproduct_set__product")
        return render(request, "debt_customer_list.html", {"debts":debts}, )  

    def post(self, request):
        debt_id = request.POST.get("debt_id")
        amount = request.POST.get("amount")
        if debt_id and amount:
            debt = DebtCustomer.objects.get(id=int(debt_id))
            debt.amount -= int(amount)
            debt.payed_amount += int(amount)
            debt.save()
            return redirect("debt_customer_list")
        else:
            return redirect("debt_customer_list")
        
class ArrivedCargoListView(AdminRequiredMixin, View):
    def get(self, request):
        arrivedcargos = ArrivedCargo.objects.all().order_by("-id").select_related("user").prefetch_related("arrived_products", "arrived_products__product")
        context  = {"arrivedcargos":arrivedcargos}
        name = request.GET.get("name")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        type_of_trade = request.GET.get("type_of_trade")

        if name:
            arrivedcargos = arrivedcargos.filter(supplier__icontains = name)
            context["arrivedcargos"] = arrivedcargos
            context["name"] = name
        if start_date:
            arrivedcargos = arrivedcargos.filter(datetime__gte = start_date)
            context["arrivedcargos"] = arrivedcargos
            context["start_date"] = start_date

        if end_date:
            arrivedcargos = arrivedcargos.filter(datetime__lte= end_date)
            context["arrivedcargos"] = arrivedcargos
            context["end_date"] = end_date
        
        if type_of_trade:
            arrivedcargos = arrivedcargos.filter(type_of_trade=type_of_trade)
            context["arrivedcargos"] = arrivedcargos
            context["type_of_trade"] = type_of_trade
        return render(request, "arrivedcargo_list.html", context)
    
class CustomerListView(AdminRequiredMixin, View):
    def get(self, request):
        customers = Customer.objects.all().order_by("-id").select_related("user").prefetch_related("selledproduct_set", "selledproduct_set__product", "selledproduct_set__customer")
        context = {"customers":customers, "title":"Sotilgan mahsulotlar"}
        name = request.GET.get("name")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        type_of_trade = request.GET.get("type_of_trade")

        if name:
            customers = customers.filter(name__icontains = name)
            context["customers"] = customers
            context["name"] = name
        if start_date:
            customers = customers.filter(datetime__gte = start_date)
            context["customers"] = customers
            context["start_date"] = start_date

        if end_date:
            customers = customers.filter(datetime__lte= end_date)
            context["customers"] = customers
            context["end_date"] = end_date
        
        if type_of_trade:
            customers = customers.filter(type_of_trade=type_of_trade)
            context["customers"] = customers
            context["type_of_trade"] = type_of_trade
        return render(request, "customer_list.html", context)
    
class DashboardView(AdminRequiredMixin, View):
    def get(self, request):
        customers = Customer.objects.filter(datetime__date = datetime.now().date())
        debtcustomers = DebtCustomer.objects.filter(created__date = datetime.now().date())
        number_of_debts = DebtCustomer.objects.all().count()
        number_of_customers = Customer.objects.all().count()
        number_of_reals = number_of_customers - number_of_debts
        try:
            todays_sells = Customer.objects.filter(datetime__date=datetime.now().date()).count()
            yesterday_sells = Customer.objects.filter(datetime__date=datetime.now()-timedelta(days=2)).count()

            farq = (todays_sells / yesterday_sells) * 100

            bugungi_tushum = Customer.objects.filter(datetime__date=datetime.now().date()).aggregate(Sum("amount"))
            kechagi_tushum = Customer.objects.filter(datetime__date=datetime.now().date()-timedelta(days=2)).aggregate(Sum("amount"))
            tushum_farq = (bugungi_tushum["amount__sum"] / kechagi_tushum["amount__sum"]) * 100
        except:
            todays_sells = 000
            farq = "--"
            bugungi_tushum = 00
            tushum_farq = "---"
        context = {
            "customers":customers,
            "debtcustomers":debtcustomers,
            "number_of_debts":number_of_debts,
            "number_of_reals":number_of_reals,
            "todays_sells":todays_sells,
            "farq":farq, 
            "bugungi_tushum":bugungi_tushum,
            "tushum_farq":tushum_farq
        }
        return render(request, "dashboard.html", context)   