from django.urls import path
from . import views

urlpatterns = [
    path("service_images/", views.service_images_view, name="service_images"),
]
