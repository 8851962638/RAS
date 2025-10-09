from django.db import models
from django.contrib.auth.models import User 


class ServiceImage(models.Model):
    id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service_images/')
    type_of_art = models.CharField(max_length=100)
    file_url = models.URLField(blank=True, null=True)
    userupload_id = models.IntegerField(default=0)  # if you just want to store an ID manually
    userupload_name = models.CharField(max_length=255, default="Anonymous", null=False, blank=False)  # uploader’s name as text

    class Meta:
        db_table = "service_images"

    def __str__(self):
        return f"{self.image_name} ({self.type_of_art})"
