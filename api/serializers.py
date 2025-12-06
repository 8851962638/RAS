
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
