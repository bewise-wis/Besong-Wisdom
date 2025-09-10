from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api import ProjectViewSet, SkillViewSet, BlogPostViewSet
from django.conf import settings  # Add this import
from django.conf.urls.static import static  # Add this import

router = DefaultRouter()
router.register(r'api/projects', ProjectViewSet)
router.register(r'api/skills', SkillViewSet)
router.register(r'api/blog', BlogPostViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_post, name='blog_post'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('', include(router.urls)),
]

# Add this at the end to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)