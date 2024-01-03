from django.urls import path
from .views import DebtArrivedCargoListView, DebtCustomerListView, ArrivedCargoListView, CustomerListView, DashboardView


urlpatterns = [
    path("mening-qarzlarim/", DebtArrivedCargoListView.as_view(), name="debt_arrived_cargo_list"),
    path("mijoz-qarzlari/", DebtCustomerListView.as_view(), name="debt_customer_list"),

    path("kelgan-mahsulotlar-royhati/", ArrivedCargoListView.as_view(), name="arrivedcargo_list"),
    path("sotilgan-mahsulotlar-royhati/", CustomerListView.as_view(), name="customer_list"),


    path("dashboard/", DashboardView.as_view(), name="dashboard"),

]