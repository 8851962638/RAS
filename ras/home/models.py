from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Booking(models.Model):
    id = models.AutoField(primary_key=True)   # Primary key
    booking_id = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_user_id = models.IntegerField()  
    service_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    total_walls = models.IntegerField()
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    total_sqft = models.DecimalField(max_digits=12, decimal_places=2)
    appointment_date = models.DateField()
    design_names = models.TextField(blank=True, null=True)
    type_of_art_booked = models.CharField(max_length=100)
    customer_design = models.ImageField(upload_to='customer_designs/', blank=True, null=True)
    price_of_design = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Payment-related fields
    payment_option = models.CharField(max_length=50, default='Razorpay')  # free text field
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "booking"

    def __str__(self):
        return f"{self.booking_id} - {self.service_name}"
    



class Review(models.Model):
    id = models.BigAutoField(primary_key=True)   # Explicit primary key
    customer_id = models.CharField(max_length=50)  # Custom customer id

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_review = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "review"

    def __str__(self):
        return f"{self.customer_name} - Review"


# models.py
from django.db import models
from django.conf import settings

class CustomProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    other_material = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Custom Product ({self.user})"
