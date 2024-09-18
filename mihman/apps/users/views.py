from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import CustomUser

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        mb_number_or_email = request.POST.get('email_or_mobile')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')

        if name and mb_number_or_email and password and re_password:
            if CustomUser.objects.filter(username=name).exists():
                return render(request, 'register.html', {'message_username': "This username is already taken"})
            
            if CustomUser.objects.filter(mb_number_or_email=mb_number_or_email).exists():
                return render(request, 'register.html', {'message_number': "This mobile number is already taken"})
            
            if password != re_password:
                return render(request, 'register.html', {'message_password': "Passwords must match"})
            
            try:
                user = CustomUser.objects.create_user(username=name, mb_number_or_email=mb_number_or_email, password=password)
                user = authenticate(username=name, password=password)
                
                if user is not None:
                    auth_login(request, user)
                    return redirect('users:home')
                else:
                    messages.info(request, 'Authentication failed.')
                    return render(request, 'users/register.html')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
                return render(request, 'users/register.html')

    return render(request, 'users/register.html')

def login(request):
    if request.method == 'POST':
        mb_number_or_email = request.POST.get('email_or_mobile')
        password = request.POST.get('password')

        user = authenticate(username=mb_number_or_email, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('users:home')
        else:
            error_message = 'Invalid username or password'
            return render(request, "users/login.html", {'error_message': error_message})
    
    return render(request, "users/login.html")

def logout(request):
    auth_logout(request)
    return redirect('users:home')

def conditions_of_use(request):
    return render(request, 'users/conditions_of_use.html')

def privacy_notice(request):
    return render(request, 'users/privacy_notice.html')

def need_help(request):
    return render(request, 'users/need_help.html')

def profile(request):
    user = CustomUser.objects.get(username=request.user.username)
    context = {"CustomUser": user}
    return render(request, 'users/profile.html', context)
