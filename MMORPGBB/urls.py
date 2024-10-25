
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from board.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('admin/', admin.site.urls),
    path('board/', include('board.urls')),
    path('auth/', include('sign.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)