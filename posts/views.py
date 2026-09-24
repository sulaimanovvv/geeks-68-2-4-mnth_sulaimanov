from typing import Any

from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.http.request import HttpRequest
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.db.models import Q, QuerySet
from django.db.models import Model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .models import Post, Tag, Category
from .forms import PostForm


class HelloWorldView(View):
    def get(self, request):
        return HttpResponse("<h1>Hello world!</h1>")

class MyNameView(View):
    def get(self, request):
        return HttpResponse('<h1>Imran</h1>')
    
class SayNameView(View):
    def get(self, request, name):
        return HttpResponse(f'<h1>Hello, {name}</h1>')


class PostListView(ListView):
    model = Post
    template_name = "list_posts.html"
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        posts = Post.objects.filter(is_published=True)
        
        search = self.request.GET.get('search')
        selected_tags = self.request.GET.getlist('tag')
        selected_category = self.request.GET.get('category')
        
        
        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(text__icontains=search)
            )
            
        if selected_category:
            posts = posts.filter(category_id=selected_category)
        
        if selected_tags:
            posts = posts.filter(
                tags__id__in=selected_tags
            ).distinct()
            
        return posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        context['selected_category'] = self.request.GET.get('category')
        context['selected_tags'] = self.request.GET.getlist('tag')

        return context
    
    
class MyPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/my_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    
    
class PostDetailView(DetailView):
    model = Post
    template_name = "post/post_detail.html"
    context_object_name = 'post'

    def get_object(self, queryset: QuerySet[Any, Any] | None = None)-> Model:
        post = super().get_object(queryset)
        post.views += 1
        post.save(update_fields=['views'])
        return post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/create_post.html'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_published = True
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['categories'] = Category.objects.all()
        
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post 
    template_name = 'post/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')
    
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)



class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/edit_post.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)