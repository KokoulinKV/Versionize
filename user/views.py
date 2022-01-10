from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.forms import UserLoginForm
from user.models import User


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        email = request.POST['email']
        username = User.objects.get(email=email)
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('user:lk'))
    else:
        form = UserLoginForm()
    context = {'title': 'Login',
               'form': form}
    return render(request, 'user/login.html', context)




# Вернуть, когда будет создано основное приложение
# def lk(request):
#     return render(request, 'user/lk.html')
