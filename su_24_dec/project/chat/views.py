from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('superuser_dashboard')
            return redirect('user_dashboard')
    return render(request, 'login.html')

@login_required
def superuser_dashboard(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')
    users = User.objects.filter(is_superuser=False)
    return render(request, 'superuser.html', {'users': users})

@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return redirect('superuser_dashboard')
    return render(request, 'user.html')

@login_required
def private_chat(request, room_name):
    return render(request, 'private_chat.html', {'room_name': room_name})
