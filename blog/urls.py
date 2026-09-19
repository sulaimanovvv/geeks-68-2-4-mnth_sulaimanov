"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from posts.views import hello_world, my_name, say_name, post_list, my_posts, post_detail, create_post, delete_post, edit_post
from user.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello/", hello_world),
    path("name/", my_name),
    path("name/<str:name>", say_name),
    path("", post_list, name='post_list'),
    path('my-posts/', my_posts, name='my_posts'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/create/', create_post, name='create_post'),
    path('post/<int:pk>/delete',delete_post, name='delete_post' ),
    path('post/<int:pk>/edit/', edit_post, name='post_edit'),
    path('accounts/register', register, name='register'),
    path('accounts/', include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
