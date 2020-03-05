from django.urls import path
from .views import PostView, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('new/', PostCreate.as_view(), name='post-new'),
    path('<slug:slug>/update', PostUpdate.as_view(), name='post-update'),
    path('<slug:slug>/delete', PostDelete.as_view(), name='post-delete'),
    path('<slug:slug>/', PostView.as_view(), name='post-view'),
]