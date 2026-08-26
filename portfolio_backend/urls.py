"""
URL configuration for portfolio_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def root_health_check(request):
    """
    Root health check endpoint for Render / Deployment platforms.
    Returns 200 OK for GET / and HEAD / health checks.
    """
    return JsonResponse({
        "status": "online",
        "service": "Kuldeep AI Portfolio Backend API",
        "version": "1.0.0",
        "endpoints": {
            "api_root": "/api/",
            "admin_panel": "/admin/"
        }
    })

urlpatterns = [
    path('', root_health_check, name='root-health-check'),
    path('admin/', admin.site.urls), # Admin Panel
    path('api/', include('api.urls')), # API routes
]

# Allow media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)