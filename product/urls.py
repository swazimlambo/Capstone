from django.urls import path
from .views import ProductCreate, ProductList, ProductRetrieveUpdateDestroy, CategoryListCreate, CategoryDetail

urlpatterns = [
    #Products
    path('products/<int:pk>/', ProductRetrieveUpdateDestroy.as_view(), name='product_detail'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/create/', ProductCreate.as_view(), name='product_create'),

    #Categories
    path('categories/', CategoryListCreate.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
]