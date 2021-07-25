from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('captcha/', include('captcha.urls')),
]


# Для режима отладки, чтобы в локалке показывались медиа-файлы
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
