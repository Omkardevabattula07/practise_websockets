# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message



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
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('user_list')
#         else:
#             messages.error(request, "Invalid username or password")
#     return render(request, 'login.html')

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('user_list')
#     return render(request, 'chat/login.html')

@login_required
def user_dashboard(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'users': users})

@login_required
def superuser_dashboard(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'superuser_list.html', {'users': users})
# @login_required
# def private_chat(request, username):
#     other_user = User.objects.get(username=username)
#     room_name = f'private_{min(request.user.username, other_user.username)}_{max(request.user.username, other_user.username)}'
#     return render(request, 'chat_room.html', {
#         'room_name': room_name,
#         'other_user': other_user,
#     })

@login_required
def private_chat(request, username):
    other_user = User.objects.get(username=username)
    room_name = f'private_{min(request.user.username, other_user.username)}_{max(request.user.username, other_user.username)}'

    # Fetch all messages for this room
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    )

    return render(request, 'chat_room.html', {
        'room_name': room_name,
        'other_user': other_user,
        'messages': messages,
    })
