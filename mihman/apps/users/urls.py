from django.urls import path,include
from apps.users import views

app_name = "users"

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('conditions_of_use/', views.conditions_of_use, name='conditions_of_use'),
    path('privacy_notice/', views.privacy_notice, name='privacy_notice'),
    path('need_help/', views.need_help, name='need_help'),
    path('profile/', views.profile, name='profile'),
]