from django.urls import path
from .views import api_save_custom_product, save_customer_signup_api, verify_customer_otp_api, save_employee_signup_api, verify_employee_otp_api, login_api, api_create_order, api_verify_payment
from .views import api_get_customer_profile, api_update_customer_profile
from .views import api_get_employee_profile, api_update_employee_profile
app_name = "api"

urlpatterns = [
    path('signup_api/', save_customer_signup_api, name='customer_signup'),
    path('verify_otp/', verify_customer_otp_api, name='verify_customer_otp'),
    path('signup_api_emp/', save_employee_signup_api, name='employee_signup'),
    path('verify_otp_emp/', verify_employee_otp_api, name='verify_employee_otp'),
    path('login_api/', login_api, name='login_api'),
    path("wallet/create-order/", api_create_order, name="api_create_order"),
    path("wallet/verify-payment/", api_verify_payment, name="api_verify_payment"),
    path("customer/profile/", api_get_customer_profile),
    path("customer/profile/update/", api_update_customer_profile),

    path("employee/profile/", api_get_employee_profile),
    path("employee/profile/update/", api_update_employee_profile),
    path("custom-product/save/", api_save_custom_product),

]
