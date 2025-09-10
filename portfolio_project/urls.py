from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.admin import custom_admin_site  # Import your custom admin site

urlpatterns = [
    path('admin/', custom_admin_site.urls),  # Use custom admin
    path('summernote/', include('django_summernote.urls')),
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Optional: If you want to keep the default admin accessible at a different URL
# urlpatterns.append(path('default-admin/', admin.site.urls))