from django.db import models
from django.core.validators import URLValidator
from taggit.managers import TaggableManager
from django_summernote.fields import SummernoteTextField

class Profile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    about_me = models.TextField( blank=True)
    profile_picture = models.ImageField(upload_to='profiles/')
    about_picture = models.ImageField(upload_to='profiles/' , default='profiles/default_about.jpg')
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    linkedin = models.TextField(validators=[URLValidator()], blank=True)
    github = models.TextField(validators=[URLValidator()], blank=True)
    twitter = models.TextField(validators=[URLValidator()], blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    project_url = models.TextField(validators=[URLValidator()], blank=True)
    github_url = models.TextField(validators=[URLValidator()], blank=True)
    technologies = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=50)  # 0-100%
    category = models.CharField(max_length=100)  # e.g., Frontend, Backend, etc.
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_position = models.CharField(max_length=100, blank=True)
    client_company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(choices=[(i, f'{i} Star') for i in range(1, 6)])  # 1-5 stars
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial from {self.client_name}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = SummernoteTextField()
    excerpt = models.TextField(max_length=300)
    featured_image = models.ImageField(upload_to='blog/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"