from django.db import models
from db_conn import db
import uuid

# Create your models here.

employees = db['Employee']

class Employee(models.Model):
    employee_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False # Prevents the ID from being changed in the Django admin or forms
    )
    fullName = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    
    # string representation of employee model
    def __str__(self):
        return self.fullName