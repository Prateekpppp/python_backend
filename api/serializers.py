from rest_framework import serializers
from employees.models import Employee
from employees.models import Employeeattendance

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        
class AttendanceSerializer(serializers.ModelSerializer):
    # employee_id = serializers.CharField()
    # date = serializers.CharField()
    # status = serializers.IntegerField()
    class Meta:
        model = Employeeattendance
        fields = "__all__"
        
        
# class EmployeeattendanceSerializer(serializers.Serializer):
#     employee_id = serializers.CharField()
#     fullName = serializers.CharField()
#     attendance = AttendanceSerializer(many=True)