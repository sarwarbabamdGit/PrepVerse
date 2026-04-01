from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .views import is_admin

@user_passes_test(is_admin)
def create_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()
            messages.success(request, f"Admin user {username} created successfully.")
            return redirect('adminpanel:users')
            
    return render(request, 'adminpanel/create_admin.html')
