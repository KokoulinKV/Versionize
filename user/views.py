from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView

from user.forms import UserLoginForm
from user.models import User


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse('main:index', args=(self.request.user.id,))

# def login(request):
#     try:
#         user_error = False
#         if request.method == 'POST':
#             form = UserLoginForm(data=request.POST)
#             email = request.POST['email']
#             username = User.objects.get(email=email)
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('main:index', args=(user.id,)))
#         else:
#             form = UserLoginForm()
#     except:
#         form = UserLoginForm()
#         user_error = True
#     context = {'title': 'Login',
#                'form': form,
#                'user_error': user_error}
#     return render(request, 'user/login.html', context)


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('user:login'))
class UserLogoutView(LogoutView):
    next_page = '/'