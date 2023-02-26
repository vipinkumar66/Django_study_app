from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Room, Topic, User, Messages
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def loginfunc(request): #here we are getting the details of the person like username, password ffrom the post request which he sent and then we are checking the user with that name is present in the system or not, if he is then we will authenticate him by checking his username,password and then we will login him if he is authenticated and if anything goes wrong here we are just going to display a flash message and then return him to same page
    page = 'login' 
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user doesn't exists")

        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect ("home")
        messages.error(request, "Wrong credentials")
    return render(request, 'login_reg.html', {'page':page})

def logoutfunc(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #this wont save the data but will keep for sometime so that we can access that user and do some changes to it.
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, 'An error occured during Registration Process')

    return render(request, 'login_reg.html', {'form':form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | 
                                Q(name__icontains=q))
    topics = Topic.objects.all()
    messages = Messages.objects.filter(Q(room__topic__name__icontains = q))
    return render (request, 'home.html', {'rooms':rooms, 'topics':topics, 'all_messages':messages})

def room(request, pk): #this function teaches how to work with the string parameters which are passed into the url
    room = Room.objects.get(id=pk)
    messages = room.messages_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        messages = Messages.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user) #when a user comment under a room this will make sure that the user gets added to the participants list
        return redirect('room', pk=room.id)
    return render(request, 'room.html', {'room':room, 'room_messages':messages, 'participants':participants})

@login_required(login_url='login_reg')
def create_room(request):
    form = RoomForm() #here we are creating the instance of the form here we dont have any data inside it
    if request.method == "POST":
        form = RoomForm(request.POST) #whatever data we are going to recieve from the user here we are going to pass it to the forms and the django model forms are smart to understand which data should be passed where.
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'create_room.html', {'form':RoomForm})

@login_required(login_url='login_reg')
def update_room(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("<h2>You are not allowed here!!</h2>")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect ('login_reg')
    return render(request, 'update_room.html', {'form':form})

@login_required(login_url='login_reg')
def delete_room(request, pk):
    #here we can also create our own html page for this and just use the request part here that whether the request is to post then we delete it, this form will be acting as a confirmation for the deletion part
    room = Room.objects.get(id=pk)
    room.delete()
    return redirect('home')

# @login_required(login_url='login_reg')
# def delete_message(request, pk):
#     del_message = Messages.objects.get(id=pk)
#     del_message.delete()
#     return redirect('home')
    
def profilepage(request, username):
    user = User.objects.get(username = username)
    messages = user.messages_set.all()
    room = user.room_set.all()
    return render(request, 'profile.html', {'all_messages':messages, "rooms":room, "user":user})