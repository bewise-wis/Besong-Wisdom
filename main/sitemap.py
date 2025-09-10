# sitemap.py
from django.contrib.sitemaps import Sitemap
from .models import Project, BlogPost

class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return BlogPost.objects.filter(published=True)