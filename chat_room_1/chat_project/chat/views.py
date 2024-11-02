from django.shortcuts import render
from .models import Message
# Create your views here.


def chat_room (request,room_name):
    message = Message.objects.filter(room_name=room_name)
    return render (request , 'chat_room.html',{ 'room_name':room_name,'message':message})