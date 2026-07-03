"""
URL configuration for ging_profile_v2 project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
import os

def serve_vue_frontend(request):
    dist_path = settings.BASE_DIR / 'portfolio' / 'dist'
    index_file = dist_path / 'index.html'
    
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/html')
    return HttpResponse("Frontend not built. Run 'npm run build' in portfolio directory.", status=503)

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('users.urls')),
]

# Serve Vue frontend in production
if not settings.DEBUG and os.path.exists(settings.BASE_DIR / 'portfolio' / 'dist'):
    urlpatterns += [
        re_path(r'^(?!api/|static/|media/|django-admin/).*$', serve_vue_frontend, name='vue_frontend'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
