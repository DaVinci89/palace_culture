from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('events/', include('events.urls')),
    path('collectives/', include('collectives.urls')),
    path('gallery/', include('gallery.urls')),
    path('news/', include('news.urls')),
    path('users/', include('users.urls')),
    path('about/', include('about.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
