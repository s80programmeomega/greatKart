
from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_categories'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product_detail'),
    path('product/', views.product_list, name='product_list'),
    path('product/add/', views.product_create, name='product_create'),
    path('product/<int:id>/', views.product_update, name='product_update'),
    path('product/delete/<int:id>/', views.product_delete, name='product_delete'),
    path('search/', views.search, name='search'),
]
