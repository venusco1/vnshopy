from django.urls import path
from apps.products import views

app_name = "products"

urlpatterns = [
    path('', views.products, name='products'),
    path('category/<int:category_id>/', views.products, name='products_by_category'),
    path('subcategory/<int:subcategory_id>/', views.products, name='products_by_subcategory'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

]
