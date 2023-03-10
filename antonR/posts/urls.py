from django.urls import path

from . import views


app_name = 'posts'

urlpatterns = [
    path('post/', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
]
