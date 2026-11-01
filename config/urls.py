from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def favicon_view(request):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#0f172a" stroke="#ef4444" stroke-width="4"/><text x="50" y="65" font-size="50" font-family="sans-serif" font-weight="bold" fill="#ef4444" text-anchor="middle">U</text></svg>'
    return HttpResponse(svg, content_type="image/svg+xml")

urlpatterns = [
    path('favicon.ico', favicon_view, name='favicon'),
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
