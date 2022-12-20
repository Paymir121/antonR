# ice_cream/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index),
    # Страница со списком сортов мороженого
    path('build_proj/', views.build_proj_list),
    # Отдельная страница с информацией о сорте мороженого
    path('build_proj/<pk>/', views.build_proj_detail),
]