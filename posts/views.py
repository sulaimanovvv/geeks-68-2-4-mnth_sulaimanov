from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from .models import Post, Tag, Category
from .forms import PostForm
from django.db.models import Q

def hello_world(request):
    return HttpResponse("<h1>Hello world!</h1>")

def my_name(request):
    name = "Imran"
    return HttpResponse(f"<h2> Hello </h2> <h1>{name}</h1>")

def say_name(request, name):
    return HttpResponse(f"<h2> Hello </h2> <h1>{name}</h1>")


def post_list(request: HttpResponse):
    qp = request.GET
    posts = Post.objects.filter(is_published=True).order_by('id')

    if search := qp.get('search'):
        title = Q(title__icontains=search)
        text = Q(text__icontains=search)
        posts = posts.filter(title | text)
    
    posts = posts[0:5]
    return render(request, "list_posts.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.views += 1
    post.save()
    return render(request, 'post/post_detail.html', {'post': post})


def create_post(request: HttpRequest) -> HttpResponse:
    if request.method.lower() == 'post':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.is_published = True
            post.save()
            form.save_m2m()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    tags = Tag.objects.all()
    category = Category.objects.all()

    return render(request, 'post/create_post.html', {
        'form': form,
        'tags': tags,
        'categories': category,
    })



def delete_post(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, id=pk)
    
    if request.method.lower() == 'post':
        post.delete()
        
        return redirect('post_list')
    
    return render(request, 'post/delete_post.html', context={'post': post})


