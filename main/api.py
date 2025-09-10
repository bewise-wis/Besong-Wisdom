from rest_framework import viewsets
from .models import Project, Skill, BlogPost
from .serializers import ProjectSerializer, SkillSerializer, BlogPostSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer