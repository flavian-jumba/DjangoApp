from django.shortcuts import render
from .models import Room 

def home(request):
    roomsdata = Room.objects.all()
    context = {'rooms': roomsdata}
    return render(request, 'baseapp/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'baseapp/room.html', context)


def createRoom(request):
    context = {}
    return render(request, 'baseapp/create_room.html', context)