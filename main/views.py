from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import never_cache

from .models import Profile, Project, Skill, Testimonial, BlogPost, ContactMessage
from .forms import ContactForm
@never_cache
def index(request):
    profile = cache.get('profile')
    if not profile:
        profile = Profile.objects.first()
        cache.set('profile', profile, 60*60*24)
    
    featured_projects = cache.get('featured_projects')
    if not featured_projects:
        featured_projects = Project.objects.filter(featured=True)[:3]
        cache.set('featured_projects', featured_projects, 60*60*12)
    
    skills = Skill.objects.all()
    testimonials = Testimonial.objects.filter(featured=True)[:3]
    latest_posts = BlogPost.objects.filter(published=True)[:3]
    
    # Handle contact form submission if it's a POST request
    if request.method == 'POST' and 'name' in request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            
            # Send email notification
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                try:
                    email_subject = f"Portfolio Contact: {form.cleaned_data['subject']}"
                    email_message = f"""
                    New message from your portfolio contact form:
                    
                    Name: {form.cleaned_data['name']}
                    Email: {form.cleaned_data['email']}
                    Subject: {form.cleaned_data['subject']}
                    
                    Message:
                    {form.cleaned_data['message']}
                    
                    Sent: {time.strftime('%Y-%m-%d %H:%M:%S')}
                    """
                    
                    send_mail(
                        email_subject,
                        email_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.DEFAULT_FROM_EMAIL],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Email sending failed: {e}")
            
            # Add success message
            messages.success(request, 'Your message has been sent successfully! I will get back to you soon.')
            return redirect('index#contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    return render(request, 'main/index.html', {
        'profile': profile,
        'featured_projects': featured_projects,
        'skills': skills,
        'testimonials': testimonials,
        'latest_posts': latest_posts,
        'form': form
    })

# Add a signal to clear cache when profile is updated
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Profile)
def clear_profile_cache(sender, instance, **kwargs):
    """Clear cache when profile is updated"""
    cache.delete('profile')
    # You might want to clear other caches that include profile data

def projects(request):
    all_projects = Project.objects.all().order_by('-date_created')
    
    # Pagination
    paginator = Paginator(all_projects, 6)  # Show 6 projects per page
    page = request.GET.get('page')
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        projects = paginator.page(paginator.num_pages)
    
    context = {
        'projects': projects,
        'page_obj': projects,  # For consistency with previous code
    }
    return render(request, 'main/projects.html', context)

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    context = {'project': project}
    return render(request, 'main/project_detail.html', context)

def blog(request):
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/blog.html', {'page_obj': page_obj})

def blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, 'main/blog_post.html', {'post': post})

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Project.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(technologies__icontains=query)
        )
    return render(request, 'main/search.html', {'results': results, 'query': query})

@require_http_methods(["GET", "POST"])
def contact(request):
    profile = Profile.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Save to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            
            # Send email notification
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                try:
                    email_subject = f"Portfolio Contact: {subject}"
                    email_message = f"""
                    New message from your portfolio contact form:
                    
                    Name: {name}
                    Email: {email}
                    Subject: {subject}
                    
                    Message:
                    {message}
                    
                    Sent: {time.strftime('%Y-%m-%d %H:%M:%S')}
                    """
                    
                    send_mail(
                        email_subject,
                        email_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.DEFAULT_FROM_EMAIL],  # Send to yourself
                        fail_silently=False,
                    )
                except Exception as e:
                    # Log error but don't break the form submission
                    print(f"Email sending failed: {e}")
            
            # Add success message
            messages.success(request, 'Your message has been sent successfully! I will get back to you soon.')
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
            else:
                return redirect('contact')
        else:
            # Form is invalid
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - show empty form
        form = ContactForm()
    
    return render(request, 'main/contact.html', {
        'form': form,
        'profile': profile
    })