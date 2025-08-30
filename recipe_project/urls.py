from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('', include('apps.categories.urls')),
    path('', include('apps.ingredients.urls')),
    path('', include('apps.recipes.urls')),
    path('', include('apps.users.urls')),
    
    # DRF Browsable API
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
