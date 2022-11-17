from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.validators import validate_email

User = get_user_model()

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        error = False
        if not username or User.objects.filter(username=username).first():
            messages.error(request, 'Username not entered or username already exists.')
            error = True
        if not email or User.objects.filter(email=email).first():
            messages.error(request, 'Email not entered or user with this email already exists.')
            error = True
        else:
            try:
                validate_email(email)
            except:
                messages.error(request, 'Invalid email.')
                error = True
        if not password or not password2 or password != password2:
            messages.error(request, 'Passwords not entered, or do not match.')
            error = True
        if not error:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f'User {username} registration successful. You can log in now.')
            return redirect('login')
        
    return render(request, 'user_profile/register.html')
