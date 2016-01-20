from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html', {})


def register(request):
    print('RECEIVED REQUEST: ' + request.method)
    notifications = []
    if request.method == 'GET':
      if request.user.is_authenticated():
          notifications.append("Вече сте логнат.")
          return redirect('/')
      return render(request, 'register.html', {})
    else:
      if request.user.is_authenticated():
        notifications.append("Вече сте логнат.")
        return render(request, 'index.html', {'messages': notifications})
      user = User.objects.create_user(request.POST['username'],
                                      request.POST['email'],
                                      request.POST['password'])
      notifications.append("Регистрира се. Животът е хубав.")
      return render(request, 'index.html', {'messages': notifications})

def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    notifications = []
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'index.html', {})
        else:
            notifications.append(username + " акаунтът е неактивен.")
    else:
        notifications.append("Невалидно име или парола.")
        return render(request, 'index.html', {'messages': notifications})

def user_logout(request):
    logout(request)
    return render(request, 'index.html', {})