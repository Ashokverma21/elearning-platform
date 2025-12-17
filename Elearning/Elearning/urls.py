from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from courses.views import stream_video

def default_redirect(request):
    return redirect('login')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', default_redirect),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path("stream/<path:path>/", stream_video, name="stream_video"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
