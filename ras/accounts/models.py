from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=150, null=True, blank=True)
    fathers_name = models.CharField(max_length=150, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    gender = models.CharField(max_length=20, null=True, blank=True)  

    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email_address = models.EmailField(unique=True, null=True, blank=True)

    house_no = models.CharField(max_length=50, null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    aadhar_card_no = models.CharField(max_length=12, unique=True, null=True, blank=True)
    aadhar_card_image_front = models.ImageField(upload_to="aadhar_cards/front/", null=True, blank=True)
    aadhar_card_image_back = models.ImageField(upload_to="aadhar_cards/back/", null=True, blank=True)

    # Extra fields
    experience = models.PositiveIntegerField(null=True, blank=True, help_text="Experience in years")
    type_of_work = models.CharField(max_length=100, null=True, blank=True)
    preferred_work_location = models.CharField(max_length=100, null=True, blank=True)
    passport_photo = models.ImageField(upload_to="passport_photos/", null=True, blank=True)

    bank_account_holder_name = models.CharField(max_length=150, null=True, blank=True)
    account_no = models.BigIntegerField(unique=True, null=True, blank=True)
    ifsc_code = models.CharField(max_length=15, null=True, blank=True)

    password = models.CharField(max_length=128, null=True, blank=True) 
    role = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "Employee"
    
    def __str__(self):
        return self.full_name or "Unnamed Person"
