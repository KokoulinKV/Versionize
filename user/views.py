from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.forms import UserLoginForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(username=email, password=password)
            if user and user.is_active:
                auth.login(request, user)
                # return HttpResponseRedirect(reverse('lk')) - вернуть, когда будет создано основное приложение
                return HttpResponseRedirect(reverse(''))
    else:
        form = UserLoginForm()
    context = {'title': 'Login',
               'form': form}
    return render(request, 'user/login.html', context)

# Вернуть, когда будет создано основное приложение
# def lk(request):
#     return render(request, 'user/lk.html')
