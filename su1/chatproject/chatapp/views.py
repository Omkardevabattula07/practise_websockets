from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .models import Message
# from django.utils.decorators import sync_to_async
from hashlib import sha256

@login_required
def user_redirect(request):
    if request.user.is_superuser:
        return redirect('superuser_page')
    return redirect('normal_user_page')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('user_redirect')
    return render(request, 'login.html')

@login_required
def superuser_page(request):
    if not request.user.is_superuser:
        return redirect('normal_user_page')
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'superuser_page.html', {'users': users})

@login_required
def normal_user_page(request):
    return render(request, 'normal_user_page.html')

@login_required
async def chat_room(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    room_name = sha256(f"{min(request.user.id, recipient.id)}_{max(request.user.id, recipient.id)}".encode()).hexdigest()

    # messages = await sync_to_async(list)(Message.objects.filter(
    #     sender_id__in=[request.user.id, recipient.id],
    #     recipient_id__in=[request.user.id, recipient.id]
    # ).order_by("timestamp"))

    return render(request, 'chat_room.html', {
        'recipient': recipient,
        'messages': messages,
        'room_name': room_name,
        'sender_id': request.user.id,
        'recipient_id': recipient.id
    })
