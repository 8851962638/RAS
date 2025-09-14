from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    # path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('customer_signup/', views.customer_signup, name='signup_customer_'),
    path('logout/', views.logout_view, name='logout'),
    path('save_signup/', views.save_signup, name='save_signup'),
    path("save_customer_signup/", views.save_customer_signup, name="save_customer_signup"),
    path('verify_customer_otp/', views.verify_customer_otp, name='verify_customer_otp'),
    path('login/', views.login_view, name='login'),
    path('loginauth/', views.login_auth, name='loginauth'),




]