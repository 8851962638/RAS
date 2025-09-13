from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),   # root: /
    path('home/', views.home_view, name='home_page'),  # /home/
    path("contact/", views.contact, name="contact"),
    path('explore/<str:service_type>/', views.explore_service, name='explore_service'),
# Correct URL pattern
    path('book/<str:service_type>/', views.book_service, name='book_service'),

]
