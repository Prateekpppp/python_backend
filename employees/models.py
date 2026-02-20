from django.db import models
from db_conn import db

# Create your models here.

employees = db['Employee']

class Employee(models.Model):
    employee_id = models.CharField(max_length=10)
    fullName = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    
    # string representation of employee model
    def __str__(self):
        return self.fullName