from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from app.models import Rider
from app.models import Event
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from app.serializers import RiderSerializer


def index(request):
    notifications = []
    if request.user.is_authenticated():
        return render(request, 'index.html', {'events': Event.objects.all()})
    else:
        return render(request, 'index.html', {})


def delete_event(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            event = Event.objects.get(id=request.GET['id'])
            if request.user.id == event.creator_id:
                event.delete()
    return redirect('/')


def create_event(request):
    print('RECEIVED REQUEST: ' + request.method)
    notifications = []
    if request.method == 'POST':
        if request.user.is_authenticated():
            event = Event(name = request.POST['name'],
                          date = request.POST['date'],
                          start_point = request.POST['start_point'],
                          start_point_coordinates = request.POST['start_point_coordinates'],
                          end_point = request.POST['end_point'],
                          end_point_coordinates = request.POST['end_point_coordinates'],
                          description = request.POST['description'],
                          noob_friendly = request.POST['noob_friendly'],
                          creator = request.user)
            event.save()
            notifications.append("Честит сбор.")
        return redirect('/')
    else:
        return redirect('/')

def register_rider(user, first_name, nickname, last_name):
    rider = Rider(user, first_name, nickname, last_name)
    rider.save()


def register(request):
    print('RECEIVED REQUEST: ' + request.method)
    notifications = []
    if request.method == 'GET':
        if request.user.is_authenticated():
            notifications.append('Вече сте логнат.')
            return redirect('/')
        return render(request, 'register.html', {})
    else:
        if request.user.is_authenticated():
            notifications.append('Вече сте логнат.')
            return render(request, 'index.html', {'messages': notifications})
        user = User.objects.create_user(request.POST['username'],
                                        request.POST['email'],
                                        request.POST['password'])
        register_rider(user.id,
                       request.POST['first_name'],
                       request.POST['nickname'],
                       request.POST['last_name'])
        notifications.append('Регистрира се. Животът е хубав.')
        return redirect('/')


def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    notifications = []
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/')
        else:
            notifications.append(username + ' акаунтът е неактивен.')
    else:
        notifications.append('Невалидно име или парола.')
        return render(request, 'index.html', {'messages': notifications})


def user_logout(request):
    logout(request)
    return redirect('/')


def user_edit(request):
    print('RECEIVED REQUEST: ' + request.method)
    notifications = []
    if not request.user.is_authenticated():
        notifications.append('Трябва да имате активна сесия, за да редактирате профил.')
        return render(request, 'index.html', {'messages': notifications})

    new_email = request.POST['new_email']
    new_first_name = request.POST['new_first_name']
    new_nickname = request.POST['new_nickname']
    new_last_name = request.POST['new_last_name']
    
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    retyped_new_password = request.POST['retyped_new_password']

    user = request.user

    notifications.append('Регистрира се. Животът е хубав.')
    return redirect('/')

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class RiderViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = RiderSerializer

def get_user_info(request):
    user = request.user
    rider = Rider.objects.raw('SELECT * FROM app_rider WHERE user_id = ' + str(user.id))[0]
    serializer = RiderSerializer(rider)
    content = JSONRenderer().render(serializer.data)
    return JSONResponse(serializer.data)