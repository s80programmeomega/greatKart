from django.urls import path

from . import views


app_name = 'category'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<int:category_id>/', views.category_detail, name='category_detail'),
    path('delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('add/', views.category_create, name='category_add'),
]