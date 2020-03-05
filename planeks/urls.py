from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from posts.views import PostList

urlpatterns = [
    path('', PostList.as_view(), name='post-list-view'),
    path('post/', include('posts.urls')),
    path('user/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
