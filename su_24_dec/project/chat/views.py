from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def base(request):
    if getattr(request, 'limited', False):
        return HttpResponseForbidden("Too many requests. Please try again after a minute.")
    return render(request, 'base.html')
# def base(request):
    # return render (request,"base.html")
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        bio = request.POST.get('bio')
        security_question = request.POST.get('security_question')
        security_answer = request.POST.get('security_answer')
        image = request.FILES.get('image')

        # Security checks
        if password != confirm_password:
            return render(request, 'register.html', {'error': "Passwords do not match"})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "Username already exists"})

        # Create user
        user = User.objects.create(username=username, password=make_password(password))
        UserProfile.objects.create(
            user=user,
            bio=bio,
            security_question=security_question,
            security_answer=make_password(security_answer),
            image=image,
        )
        return redirect('login')
    return render (request,"register.html")
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
