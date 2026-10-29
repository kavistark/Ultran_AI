from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('assistant.urls')),
    path('accounts/', include('accounts.urls')),
    path('reminders/', include('reminders.urls')),
    path('documents/', include('documents.urls')),
    path('integrations/', include('integrations.urls')),
    path('api/', include('assistant.api_urls')),
    path('api/reminders/', include('reminders.api_urls')),
    path('api/documents/', include('documents.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
