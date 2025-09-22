from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    # path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup_customer/', views.signup_customer, name='signup_customer'),
    path('logout/', views.logout_view, name='logout'),
    path("save_employee_signup/", views.save_employee_signup, name="save_employee_signup"),
    path("verify_employee_otp/", views.verify_employee_otp, name="verify_employee_otp"),
    path("save_customer_signup/", views.save_customer_signup, name="save_customer_signup"),
    path('verify_customer_otp/', views.verify_customer_otp, name='verify_customer_otp'),
    path('login/', views.login_view, name='login'),
    path('signup_employee/', views.signup_employee, name='signup_employee'),
    path('login_auth/', views.login_auth, name='loginauth'),  





]