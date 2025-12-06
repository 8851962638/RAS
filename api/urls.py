from django.urls import path
from .views import api_save_custom_product, save_customer_signup_api, verify_customer_otp_api, save_employee_signup_api, verify_employee_otp_api, login_api, api_create_order, api_verify_payment
from .views import api_get_customer_profile, api_update_customer_profile, save_booking_api, explore_service_api, session_status_api, logout_api
from .views import api_get_employee_profile, api_update_employee_profile, api_service_image_upload
from .views import api_get_employee_profile, api_update_employee_profile, api_get_all_artists, api_get_filtered_artists
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
    
    path("save-booking/", save_booking_api, name="save_booking_api"),

    path("explore/<str:service_type>/", explore_service_api, name="explore_service_api"),
    path("session-status/", session_status_api, name="session_status_api"),
    path("logout_api/", logout_api, name="logout_api"),
    path("service-image/upload/", api_service_image_upload),
    path("artists/", api_get_all_artists),
    path("artists/filter/", api_get_filtered_artists),
]
