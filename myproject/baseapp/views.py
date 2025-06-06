from django.shortcuts import render, redirect
from .models import Room 
from .forms import RoomForm

def home(request):
    roomsdata = Room.objects.all()
    context = {'rooms': roomsdata}
    return render(request, 'baseapp/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'baseapp/room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        print(request.POST)
    context = {'form': form}
    return render(request, 'baseapp/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'baseapp/room_form.html', context)