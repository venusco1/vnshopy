from django.urls import path,include
from apps.products import views

app_name = "products"

urlpatterns = [
    path('', views.products, name='products')
]
