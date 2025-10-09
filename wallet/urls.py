from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet_dashboard, name='wallet_dashboard'),
    path('create_order/', views.create_razorpay_order_wallet, name='create_wallet_order'),
    path('verify_payment/', views.verify_razorpay_payment_wallet, name='verify_wallet_payment'),
]
