from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username', '')  # Default to empty string if None
        password = request.POST.get('password', '')  # Default to empty string if None

        if username:  # Only try to lowercase if username exists
            username = username.lower()

        if not username or not password:
            messages.error(request, 'Please provide both username and password')
            return render(request, 'baseapp/login_register.html', {'page': page})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'baseapp/login_register.html', {'page': page})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid password')

    context = {'page': page}
    return render(request, 'baseapp/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')



def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()  # Normalize username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error[0])

    return render(request, 'baseapp/login_register.html', {'form': form})
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    roomsdata = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = roomsdata.count()
    context = {'rooms': roomsdata, 'topics': topics, 'room_count': room_count}
    return render(request, 'baseapp/home.html', context)


def room(request, pk):
    try:
        room = Room.objects.get(id=pk)
        context = {'room': room}
        return render(request, 'baseapp/room.html', context)
    except Room.DoesNotExist:
        messages.error(request, 'Room does not exist')
        return redirect('home')

@login_required(login_url='login')
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
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You are not allowed to edit this room.")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'baseapp/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):    
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed to delete this room.")
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'baseapp/delete.html', {'object': room})