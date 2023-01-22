from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('post/', include('posts.urls', namespace='post')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('', include('about.urls', namespace='about')),
    path('auth/', include('django.contrib.auth.urls')),
]

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

