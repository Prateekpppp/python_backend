from employees.models import Employee
from .serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from db_conn import db
import uuid


@api_view(['GET','POST'])
def employeesView(request):
    if request.method == 'GET':
        # employees = Employee.objects.all()
        employees = db['employees']
        employees = employees.find({})
        serializer = EmployeeSerializer(employees, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        try:
            data=request.data.copy()
            data['employee_id'] = str(uuid.uuid4())
            serializer = EmployeeSerializer(data=data)
            if serializer.is_valid():
                employees = db['employees']
                
                # print(serializer.validated_data)
                employees.insert_one(data)
                # serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return  e


@method_decorator(csrf_exempt, name='dispatch')
def employee(request, id):
    try:
        employees = db['employees']
        if request.method == 'GET':
            employee = employees.find_one({
                "employee_id": id
            })
            print(employee)
            return Response(employee, status=status.HTTP_200_CREATED)
        elif request.method == 'DELETE':
            employee = employees.delete_one({
                "employee_id": id
            })
            print(employee)
            return Response(status=status.HTTP_201_DELETED)
    except Exception as e:
        return  e
        
   
# @api_view(['GET'])     
# def employeeattendance(request):
    
#     try:
#         if request.method == "GET":
            