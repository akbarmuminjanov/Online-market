from django.urls import path
from .views import (IndexView, 
                    ProductCreateView, 
                    ProductListView, 
                    ProductDetailView, 
                    ProductUpdateView, 
                    ProductDeleteView, 
                    ProductArrivedCargoView,
                    ProductSellView,
                    CuctomerDetail,
                    TodaysSellsView,)


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create/", ProductCreateView.as_view(), name='create'),
    path("list/", ProductListView.as_view(), name='list'),
    path("<int:product_id>/detail/", ProductDetailView.as_view(), name='detail'),
    path("<int:product_id>/update/", ProductUpdateView.as_view(), name='update'),
    path("<int:product_id>/delete/", ProductDeleteView.as_view(), name='delete'),
    
    path("arrivedcargo/", ProductArrivedCargoView.as_view(), name="arrived_cargo"),
    path("sellproduct/", ProductSellView.as_view(), name="sell_product"),

    path("customer/<int:customer_id>/detail/", CuctomerDetail.as_view(), name="customer_detail"),

    path("todays_sells/", TodaysSellsView.as_view(), name="todays_sells"),


]