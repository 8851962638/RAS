from django.urls import path
from . import views

urlpatterns = [
    path("", views.wallet_dashboard, name="wallet_dashboard"),
    path("add/", views.add_money, name="add_money"),
    path("spend/", views.spend_money, name="spend_money"),
]
