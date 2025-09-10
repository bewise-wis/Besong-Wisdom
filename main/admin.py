from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import Profile, Project, Skill, Testimonial, BlogPost, ContactMessage

class CustomAdminSite(admin.AdminSite):
    site_header = "Portfolio Administration"
    site_title = "Portfolio Admin"
    index_title = "Dashboard"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        # Calculate statistics
        total_projects = Project.objects.count()
        featured_projects = Project.objects.filter(featured=True).count()
        total_skills = Skill.objects.count()
        total_testimonials = Testimonial.objects.count()
        featured_testimonials = Testimonial.objects.filter(featured=True).count()
        total_blog_posts = BlogPost.objects.count()
        published_blog_posts = BlogPost.objects.filter(published=True).count()
        total_contacts = ContactMessage.objects.count()
        unread_contacts = ContactMessage.objects.filter(read=False).count()
        
        # Recent activity
        recent_projects = Project.objects.all().order_by('-date_created')[:5]
        recent_messages = ContactMessage.objects.all().order_by('-timestamp')[:5]
        recent_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:5]
        
        # Chart data (simplified)
        project_data = {
            'total': total_projects,
            'featured': featured_projects,
        }
        
        message_data = {
            'total': total_contacts,
            'unread': unread_contacts,
        }
        
        context = {
            **self.each_context(request),
            'title': 'Dashboard',
            'total_projects': total_projects,
            'featured_projects': featured_projects,
            'total_skills': total_skills,
            'total_testimonials': total_testimonials,
            'featured_testimonials': featured_testimonials,
            'total_blog_posts': total_blog_posts,
            'published_blog_posts': published_blog_posts,
            'total_contacts': total_contacts,
            'unread_contacts': unread_contacts,
            'recent_projects': recent_projects,
            'recent_messages': recent_messages,
            'recent_posts': recent_posts,
            'project_data': project_data,
            'message_data': message_data,
        }
        return render(request, 'admin/dashboard.html', context)

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Admin classes
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'bio', 'about_me', 'profile_picture', 'about_picture')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Social Media', {
            'fields': ('linkedin', 'github', 'twitter'),
            'classes': ('collapse',)
        }),
        ('Documents', {
            'fields': ('resume',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        if Profile.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        return False

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'date_created', 'technologies')
    list_filter = ('featured', 'date_created')
    search_fields = ('title', 'description', 'technologies')
    list_editable = ('featured',)
    readonly_fields = ('date_created',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'technologies')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Links', {
            'fields': ('project_url', 'github_url')
        }),
        ('Settings', {
            'fields': ('featured', 'date_created')
        }),
    )

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category')
    list_editable = ('proficiency', 'category')

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating', 'featured', 'created_at')
    list_filter = ('rating', 'featured', 'created_at')
    search_fields = ('client_name', 'content')
    list_editable = ('featured',)
    readonly_fields = ('created_at',)
    
    def rating_stars(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    rating_stars.short_description = 'Rating'

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content', 'excerpt')
    list_editable = ('published',)
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'excerpt')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Metadata', {
            'fields': ('published',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'read', 'timestamp')
    list_filter = ('read', 'timestamp')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('read',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'timestamp')
    
    def mark_as_read(self, request, queryset):
        queryset.update(read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
    
    actions = [mark_as_read, mark_as_unread]

# Register models with custom admin site only (not with both)
custom_admin_site.register(Profile, ProfileAdmin)
custom_admin_site.register(Project, ProjectAdmin)
custom_admin_site.register(Skill, SkillAdmin)
custom_admin_site.register(Testimonial, TestimonialAdmin)
custom_admin_site.register(BlogPost, BlogPostAdmin)
custom_admin_site.register(ContactMessage, ContactMessageAdmin)

# OPTIONAL: If you want to keep the default admin as well, 
# comment out the registrations below
# admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Project, ProjectAdmin)
# admin.site.register(Skill, SkillAdmin)
# admin.site.register(Testimonial, TestimonialAdmin)
# admin.site.register(BlogPost, BlogPostAdmin)
# admin.site.register(ContactMessage, ContactMessageAdmin)