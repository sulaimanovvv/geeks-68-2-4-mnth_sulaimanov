from django.shortcuts import render
from django.http.response import HttpResponse


def hello_world(request):
    return HttpResponse("<h1>Hello world!</h1>")

def my_name(request):
    name = "Imran"
    return HttpResponse(f"<h2> Hello </h2> <h1>{name}</h1>")

def say_name(request, name):
    return HttpResponse(f"<h2> Hello </h2> <h1>{name}</h1>")
