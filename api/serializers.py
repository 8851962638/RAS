
from rest_framework import serializers
from employee.models import ServiceImage

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = "__all__"


from rest_framework import serializers
from accounts.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


from home.models import Booking   

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


# serializers.py
from rest_framework import serializers
from accounts.models import CustomUser

class AdminEmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "full_name",
            "email",
            "is_active",
            "date_joined",
        ]
