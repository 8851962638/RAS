from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home_view, name='home'),   # root: /
    path('home/', views.home_view, name='home_page'),  # /home/
    path("edit_profile/", views.edit_profile_view, name="edit_profile"),    
    path('explore/<str:service_type>/', views.explore_service, name='explore_service'),
    path('book/<str:service_type>/', views.book_service, name='book_service'),    
    path("reviews/", views.reviews, name="reviews"),
    path("save-review/", views.save_review, name="save_review"),
    path('logout/', views.logout_view, name='logout'),
    path("artists/", views.artists, name="artists"),
    path('bookings/', views.bookings, name='bookings'),
    path('home/save_bookings/', views.save_booking, name='save_booking'),  
    path('shop/', views.shop, name='shop'),


]
