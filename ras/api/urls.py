from django.urls import path
from .views import save_customer_signup_api, verify_customer_otp_api, save_employee_signup_api, verify_employee_otp_api, login_api 

app_name = "api"

urlpatterns = [
    path('signup_api/', save_customer_signup_api, name='customer_signup'),
    path('verify_otp/', verify_customer_otp_api, name='verify_customer_otp'),
    path('signup_api_emp/', save_employee_signup_api, name='employee_signup'),
    path('verify_otp_emp/', verify_employee_otp_api, name='verify_employee_otp'),
    path('login_api/', login_api, name='login_api'),
]
