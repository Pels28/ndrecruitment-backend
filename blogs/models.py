# # blogs/models.py
# from django.db import models
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from django.urls import reverse

# User = get_user_model()

# class Author(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = models.ImageField(upload_to='authors/', blank=True, null=True)
#     bio = models.TextField(blank=True)
    
#     def __str__(self):
#         return self.user.get_full_name() or self.user.username

# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
    
#     def __str__(self):
#         return self.name

# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#     slug = models.SlugField(unique=True)
    
#     def __str__(self):
#         return self.name

# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True)
#     description = models.TextField(blank=True)
#     content = models.TextField()
#     image = models.ImageField(upload_to='blog/', blank=True, null=True)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     categories = models.ManyToManyField(Category, blank=True)
#     tags = models.ManyToManyField(Tag, blank=True)
#     date = models.DateTimeField(default=timezone.now)
#     draft = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['-date']
    
#     def __str__(self):
#         return self.title
    
#     def get_absolute_url(self):
#         return reverse('post-detail', kwargs={'slug': self.slug})
    
#     def reading_time(self):
#         # Estimate reading time (200 words per minute)
#         word_count = len(self.content.split())
#         return max(1, round(word_count / 200))

# blogs/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from cloudinary.models import CloudinaryField  # Add this import

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField('image', folder='authors/', blank=True, null=True)  # Change to CloudinaryField
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    content = models.TextField()
    image = CloudinaryField('image', folder='blog/', blank=True, null=True)  # Change to CloudinaryField
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    date = models.DateTimeField(default=timezone.now)
    draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})
    
    def reading_time(self):
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))