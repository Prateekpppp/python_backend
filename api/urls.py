from django.urls import path
from . import views

urlpatterns = [
    path('employees',views.employeesView),
    path('employee',views.employee),
    path('employeeattendance',views.employeeattendance),
]
