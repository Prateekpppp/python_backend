from django.db import models
from django.utils import timezone
from db_conn import db
import uuid

# Create your models here.

class Employee(models.Model):
    employee_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True # Prevents the ID from being changed in the Django admin or forms
    )
    # employee_id = models.CharField(max_length=50)
    fullName = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    
    # string representation of employee model
    def __str__(self):
        return self.fullName
    
    
class Employeeattendance(models.Model):
    employee_id = models.CharField()
    # date = models.DateField(default=timezone.now)
    date = models.CharField()
    status = models.IntegerField()
    
    def __str__(self):
        return self.employee_id