from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from app.models import Rider, Event, Comment
from django.shortcuts import redirect


def index(request):
    notifications = []
    if request.user.is_authenticated():
        return render(request, 'app/index.html', {'events': Event.objects.all()})
    else:
        return render(request, 'app/index.html', {})


def delete_event(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            event = Event.objects.get(id=request.GET['id'])
            if request.user.id == event.creator_id:
                event.delete()
                return HttpResponse(content='Event deleted')
            else:
                return HttpResponse(content='Failed to delete event: not creator of the event')
        else:
            return HttpResponse(content='Failed to delete event: not authenticated')
    else:
        return HttpResponse(content='Failed to delete event')


def create_event(request):
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
            return HttpResponse(content='Event created')
        else:
            return HttpResponse(content="Failed to create event: not authenticated")
    else:
        return HttpResponse(content='Failed to create event')


def update_event(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            event = Event.get_event(id=request.POST['event_id'])
            if request.user.id == event.creator_id:
                event.name = request.POST['name']
                event.date = request.POST['date']
                event.start_point = request.POST['start_point']
                event.start_point_coordinates = request.POST['start_point_coordinates']
                event.end_point = request.POST['end_point']
                event.end_point_coordinates = request.POST['end_point_coordinates']
                event.description = request.POST['description']
                event.noob_friendly = request.POST['noob_friendly']
                event.save()
                return HttpResponse(content='Event updated')
            else:
                return HttpResponse(content='Failed to edit event: not creator of the event')
    else:
        return HttpResponse(content='Failed to update event')


def update_rider(request):
    print('RECEIVED REQUEST: ' + request.method)
    notifications = []
    if request.method == 'POST':
        if not request.user.is_authenticated():
            notifications.append("Нямате текуща сесия.")
            return render(request, 'app/index.html', {'messages': notifications})
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.set_password (request.POST['password'])
        user.save()
        rider = Rider.get_rider(id=user.id)
        rider.first_name = request.POST['first_name']
        rider.nickname = request.POST['nickname']
        rider.last_name = request.POST['last_name']
        rider.save()
        return HttpResponse(content='Rider updated')
    else:
        return HttpResponse(content='Failed to update rider')


def register_rider(user, first_name, nickname, last_name):
    rider = Rider(user, first_name, nickname, last_name)
    rider.save()


def get_rider(request):
    rider = Rider.get_rider(id=request.GET['id'])
    if rider is not None:
        return HttpResponse(content=Rider.to_json([rider]))
    else:
        return HttpResponse(content='Cannot find rider')


def register(request):
    print('RECEIVED REQUEST: ' + request.method)
    notifications = []
    if request.method == 'GET':
        if request.user.is_authenticated():
            notifications.append('Вече сте логнат.')
            return redirect('/')
        return render(request, 'app/register.html', {})
    else:
        if request.user.is_authenticated():
            notifications.append("Вече сте логнат.")
            return render(request, 'app/index.html', {'messages': notifications})
        user = User.objects.create_user(request.POST['username'],
                                        request.POST['email'],
                                        request.POST['password'])
        register_rider(user.id,
                       request.POST['first_name'],
                       request.POST['nickname'],
                       request.POST['last_name'])
        notifications.append('Регистрира се. Животът е хубав.')
        return render(request, 'app/index.html', {'messages': notifications})


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
        notifications.append("Невалидно име или парола.")
        return render(request, 'app/index.html', {'messages': notifications})


def user_logout(request):
    logout(request)
    return redirect('/')


def get_user_info(request):
    user = request.user
    rider = Rider.objects.raw('SELECT * FROM app_rider WHERE user_id = ' + str(user.id))
    return HttpResponse(content=Rider.to_json(rider))


def read_event(request):
    event_id = request.GET['id']
    event = Event.get_event(event_id)
    if event is not None:
        return HttpResponse(content=Event.to_json([event]))
    else:
        return HttpResponse(content='Cannot find event')


def get_user_events(request):
    user = request.user
    events = Event.objects.raw('SELECT * FROM app_event WHERE creator_id = ' + str(user.id))
    return HttpResponse(content=Event.to_json(events))


def read_all_events(request):
    return HttpResponse(content=Event.to_json(Event.get_all()))


def get_all_user_comments(request):
    user = request.user
    comments = Comment.objects.raw('SELECT * FROM app_comment WHERE poster_id = ' + str(user.id))
    return HttpResponse(content=Comment.to_json(comments))


def get_all_event_comments(request):
    event_id = request.GET['id']
    comments = Comment.objects.raw('SELECT * FROM app_comment WHERE event_id = ' + str(event_id))
    return HttpResponse(content=Comment.to_json(comments))