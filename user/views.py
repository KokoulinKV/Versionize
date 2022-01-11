from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.forms import UserLoginForm
from user.models import User


def login(request):
    try:
        user_error = False
        if request.method == 'POST':
            form = UserLoginForm(data=request.POST)
            email = request.POST['email']
            username = User.objects.get(email=email)
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
        else:
            form = UserLoginForm()
    except:
        form = UserLoginForm()
        user_error = True
    context = {'title': 'Login',
               'form': form,
               'user_error':user_error}
    return render(request, 'user/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('user:login'))
