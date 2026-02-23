from employees.models import Employee
from .serializers import EmployeeSerializer
from .serializers import AttendanceSerializer
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
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@csrf_exempt
@api_view(['GET','POST','DELETE'])
def employee(request, id):
    try:
        employees = db['employees']
        if request.method == 'GET':
            employee = employees.find_one({
                "employee_id": id
            })
            # print(employee)
            return Response(employee, status=status.HTTP_200_CREATED)
        elif request.method == 'DELETE':
            employee = employees.delete_one({
                "employee_id": id
            })
            return Response(status=status.HTTP_204_NO_CONTENT)
     
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
   
@api_view(['GET','POST'])     
def employeeattendance(request):
    
    try:
        if request.method == "GET":
            
            # pipeline = [
            #     {
            #         "$lookup": {
            #             "from": "attendance",
            #             "localField": "employee_id",
            #             "foreignField": "employee_id",
            #             "as": "attendance"
            #         }
            #     },
            #     {
            #         "$unwind": {
            #             "path": "$attendance",
            #             "preserveNullAndEmptyArrays": True
            #         }
            #     },
            #     {
            #         "$project": {
            #             "_id": 0,
            #             "employee_id": 1,
            #             "fullName": 1,
            #             "email": 1,
            #             "department": 1,
            #             "status": "$attendance.status",
            #             "date": "$attendance.date"
            #         }
            #     }
            # ]
            
            print("request.GET.get('date')--",request.GET.get('date'))
            date = request.GET.get('date')
            
            pipeline = [
            {
                "$lookup": {
                    "from": "attendance",
                    "let": {"empId": "$employee_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$employee_id", "$$empId"]},
                                        {"$eq": ["$date", date]}
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "attendance"
                }
            },
            {
                "$unwind": {
                    "path": "$attendance",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "employee_id": 1,
                    "fullName": 1,
                    "email": 1,
                    "department": 1,
                    "status": "$attendance.status"
                }
            }
        ]
            employees = db['employees']
            employees = list(employees.aggregate(pipeline))
            # employees = employees.aggregate(pipeline)
            # serializer = EmployeeSerializer(employees, many=True)
            print(employees)
            return Response(employees, status=status.HTTP_200_OK)
        
        elif request.method == "POST":
            
            serializer = AttendanceSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                employees = db['attendance']
                
                data = serializer.validated_data
                
                employees.update_one(
                    {
                        "employee_id": data.get("employee_id"),
                        "date": data.get("date")
                    },
                    {
                        "$set": {
                            # "status": data.get("status"),
                            "status": data['status'],
                        }
                    },
                    upsert=True
                )
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
         
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )