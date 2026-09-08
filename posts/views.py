from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Post


def hello_world(request):
    return HttpResponse("<h1>Hello world!</h1>")

def my_name(request):
    name = "Imran"
    return HttpResponse(f"<h2> Hello </h2> <h1>{name}</h1>")

def say_name(request, name):
    return HttpResponse(f"<h2> Hello </h2> <h1>{name}</h1>")


def post_list(request):
    posts = Post.objects.filter(is_published=True)
    
    return render(request, "list_posts.html", {"posts": posts})