from django.db import models

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

    # Payment-related fields
    payment_option = models.CharField(max_length=50)  # free text field
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "booking"

    def __str__(self):
        return f"{self.booking_id} - {self.service_name}"
