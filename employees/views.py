from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def employees(request):
    return HttpResponse('<h1>Hii</h1>')