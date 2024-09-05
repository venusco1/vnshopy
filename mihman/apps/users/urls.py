from django.urls import path,include
from apps.users import views

app_name = "users"

urlpatterns = [
    path('', views.home, name='home')
]
