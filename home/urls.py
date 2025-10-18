from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name = "home"

urlpatterns = [
    path('', views.home_view, name='home'),   # root: /
    path('home/', views.home_view, name='home_page'),  # /home/
    path("edit_profile/", views.edit_profile_view, name="edit_profile"),    
    path('explore/<str:service_type>/', views.explore_service, name='explore_service'),
    path('book/<str:service_type>/', views.book_service, name='book_service'),    
    path("reviews/", views.reviews, name="reviews"),
    path("save_review/", views.save_review, name="save_review"),
    path('logout/', views.logout_view, name='logout'),
    path("artists/", views.artists, name="artists"),
    path('bookings/', views.bookings, name='bookings'),
    path("bookings/update-status/<int:booking_id>/", views.update_booking_status, name="update_booking_status"),
    path('admin/bookings/<int:booking_id>/assign/', views.assign_booking, name='assign_booking'),

    path('employee/assignments/', views.employee_bookings, name='employee_bookings'),
    path('employee/assignments/<int:booking_id>/<str:action>/', views.handle_assignment_response, name='handle_assignment_response'),

    path('home/save_booking/', views.save_booking, name='save_booking'), 
    path('shop/', views.shop, name='shop'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('create_razorpay_order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('verify_razorpay_payment/', views.verify_razorpay_payment, name='verify_razorpay_payment'),
    path("save-custom-product/", views.save_custom_product, name="save_custom_product"),
    path('assign/<int:booking_id>/', views.assign_booking, name='assign_booking'), # New URL


]
