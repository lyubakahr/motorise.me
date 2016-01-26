from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from app.models import Rider, Event, Comment, Notification, Motorbike
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
                httpResponseContent = 'Event deleted'
            else:
                httpResponseContent = 'Failed to delete event: not creator of the event'
        else:
            httpResponseContent = 'Failed to delete event: not authenticated'
    else:
        httpResponseContent = 'Failed to delete event'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


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
            httpResponseContent = 'Event created'
        else:
            httpResponseContent = 'Failed to create event: not authenticated'
    else:
        httpResponseContent = 'Failed to create event'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


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
                httpResponseContent = 'Event updated'
            else:
                httpResponseContent = 'Failed to edit event: not creator of the event'
    else:
        httpResponseContent = 'Failed to update event'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def update_rider(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            httpResponseContent = 'Failed to update rider: not authenticated'
        else:
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
            httpResponseContent = 'Rider updated'
    else:
        httpResponseContent = 'Failed to update rider'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def register_rider(user, first_name, nickname, last_name):
    rider = Rider(user, first_name, nickname, last_name)
    rider.save()


def get_rider(request):
    rider = Rider.get_rider(id=request.GET['id'])
    if rider is not None:
        return HttpResponse(content=Rider.to_json([rider]), content_type='application/json')
    else:
        return HttpResponse(content='Cannot find rider', content_type='application/json')


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
    rider = Rider.get_rider(user.id)
    return HttpResponse(content=Rider.to_json([rider]), content_type='application/json')


def read_event(request):
    event_id = request.GET['id']
    event = Event.get_event(event_id)
    if event is not None:
        return HttpResponse(content=Event.to_json([event]), content_type='application/json')
    else:
        return HttpResponse(content='Cannot find event', content_type='application/json')


def read_user_events(request):
    user = request.user
    events = Event.get_user_events(user.id)
    return HttpResponse(content=Event.to_json(events), content_type='application/json')


def read_all_events(request):
    return HttpResponse(content=Event.to_json(Event.get_all()), content_type='application/json')


def get_all_user_comments(request):
    user = request.user
    comments = Comment.get_user_comments(user.id)
    return HttpResponse(content=Comment.to_json(comments), content_type='application/json')


def get_all_event_comments(request):
    event_id = request.GET['id']
    comments = Comment.get_event_comments(event_id)
    return HttpResponse(content=Comment.to_json(comments), content_type='application/json')


def post_comment(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            event = Event.get_event(request.POST['event_id'])
            reply = request.POST['reply']
            if not reply:
                reply = None
            comment = Comment(event = event,
                              poster = request.user,
                              content = request.POST['content'],
                              reply = reply)
            comment.save()
            httpResponseContent = 'Comment posted'
        else:
            httpResponseContent = 'Failed to post comment: not authenticated'
    else:
        httpResponseContent = 'Failed to post comment'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def edit_comment(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            httpResponseContent = 'Failed to edit comment: not authenticated'
        else:
            comment = Comment.get_comment(request.POST['comment_id'])
            if comment is None:
                httpResponseContent = 'Failed to edit comment: could not find comment'
            else:
                comment.content = request.POST['content']
                comment.save()
                httpResponseContent = 'Comment edited'
    else:
        httpResponseContent = 'Failed to edit comment'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def delete_comment(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            comment = Comment.objects.get(id=request.GET['id'])
            if request.user.id == comment.poster_id:
                comment.delete()
                httpResponseContent = 'Comment deleted'
            else:
                httpResponseContent = 'Failed to delete comment: not poster of the comment'
        else:
            httpResponseContent = 'Failed to delete comment: not authenticated'
    else:
        httpResponseContent = 'Failed to delete comment'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def create_notification(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            user = Rider.get_rider(id=request.POST['user'])
            from_user = Rider.get_rider(id=request.POST.get('from_user'))
            event = Event.get_event(request.POST.get('event'))
            notification_type = request.POST['notification_type']
            if notification_type not in Notification.notification_types:
                httpResponseContent = 'Failed to create notification: invalid notification type'
            else:
                notification = Notification(user = user,
                                            from_user = from_user,
                                            event = event,
                                            notification_type = notification_type)
                notification.save()
                httpResponseContent = 'Notification created'
        else:
            httpResponseContent = 'Failed to create notification: not authenticated'
    else:
        httpResponseContent = 'Failed to create notification'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def read_user_notifications(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            notifications = Notification.get_user_notifications(request.user.id)
            httpResponseContent = Notification.to_json(notifications)
        else:
            httpResponseContent = 'Failed to get notifications: not authenticated'
    else:
        httpResponseContent = 'Failed to get notifications'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def set_notification_seen(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            notification = Notification.get_user_notifications(request.user.id)
            httpResponseContent = Notification.to_json(notification)
        else:
            httpResponseContent = 'Failed to set notification seen: not authenticated'
    else:
        httpResponseContent = 'Failed to set notification seen'


def get_notification_types(request):
    if request.method  =='GET':
        if request.user.is_authenticated():
            httpResponseContent = Notification.get_notification_types_json()
        else:
            httpResponseContent = 'Failed to get notification types: not authenticated'
    else:
        httpResponseContent = 'Failed to get notification types'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def get_motorbike_types(request):
    if request.method  =='GET':
        if request.user.is_authenticated():
            httpResponseContent = Motorbike.get_moto_types_json()
        else:
            httpResponseContent = 'Failed to get motorbike types: not authenticated'
    else:
        httpResponseContent = 'Failed to get motorbike types'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def get_motorbike_manufacturers(request):
    if request.method  =='GET':
        if request.user.is_authenticated():
            httpResponseContent = Motorbike.get_moto_manufacturers_json()
        else:
            httpResponseContent = 'Failed to display motorbike manufacturers: not authenticated'
    else:
        httpResponseContent = 'Failed to display motorbike manufcaturers'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def create_motorbike(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            moto_type = request.POST['type']
            moto_manufacturer = request.POST['manufacturer']
            if moto_type not in Motorbike.moto_types:
                httpResponseContent = 'Failed to create motorbike: invalid type'
            elif moto_manufacturer not in Motorbike.moto_manufacturers:
                httpResponseContent = 'Failed to create motorbike: invalid manufacturer'
            else:
                motorbike = Motorbike(moto_type = moto_type,
                                      moto_manufacturer = moto_manufacturer,
                                      moto_model = request.POST['model'],
                                      moto_cubature = request.POST['cubature'],
                                      moto_owner = request.user)
                motorbike.save()
                httpResponseContent = 'Motorbike created'
        else:
            httpResponseContent = 'Failed to create motorbike: not authenticated'
    else:
        httpResponseContent = 'Failed to create motorbike'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def read_motorbike(request):
    motorbike_id = request.GET['id']
    motorbike = Motorbike.get_motorbike(motorbike_id)
    if motorbike is not None:
        return HttpResponse(content=Motorbike.to_json([motorbike]), content_type='application/json')
    else:
        return HttpResponse(content='Cannot find motorbike', content_type='application/json')


def update_motorbike(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            motorbike = Motorbike.get_user_motorbike()
            moto_type = request.POST['type']
            moto_manufacturer = request.POST['manufacturer']
            if moto_type not in Motorbike.moto_types:
                httpResponseContent = 'Failed to update motorbike: invalid type'
            elif moto_manufacturer not in Motorbike.moto_manufacturers:
                httpResponseContent = 'Failed to update motorbike: invalid manufacturer'
            else:
                motorbike.moto_type = moto_type
                motorbike.moto_manufacturer = moto_manufacturer
                motorbike.moto_model = request.POST['model']
                motorbike.moto_cubature = request.POST['cubature']
                if request.user.id == motorbike.owner_id:
                    motorbike.save()
                    httpResponseContent = 'Motorbike updated'
                else:
                    httpResponseContent = 'Failed to edit motorbike: not owner of the motorbike'
    else:
        httpResponseContent = 'Failed to update motorbike'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def get_user_motorbike(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            motorbike = Motorbike.get_user_motorbike(request.user.id)
            httpResponseContent = Motorbike.to_json(motorbike)
        else:
            httpResponseContent = 'Failed to get motorbike: not authenticated'
    else:
        httpResponseContent = 'Failed to get motorbike'
    return HttpResponse(content=httpResponseContent, content_type='application/json')


def delete_motorbike(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            motorbike = Motorbike.objects.get_user_motorbike()
            if request.user.id == motorbike.owner_id:
                motorbike.delete()
                httpResponseContent = 'Motorbike deleted'
            else:
                httpResponseContent = 'Failed to delete motorbike: not owner of the motorbike'
        else:
            httpResponseContent = 'Failed to delete motorbike: not authenticated'
    else:
        httpResponseContent = 'Failed to delete motorbike'
    return HttpResponse(content=httpResponseContent, content_type='application/json')