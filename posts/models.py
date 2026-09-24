from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    text = models.CharField()
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(null=True, upload_to='posts', blank=True)
    views = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"pk": self.pk})
    


class Comment(models.Model):
    author_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    
    def __str__(self):
        return f"{self.author_name}: {self.text[:30]}"
    
