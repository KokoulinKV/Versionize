from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login

from user.forms import UserLoginForm


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    form_class = UserLoginForm
    template_name = 'user/login.html'

#    def form_valid(self, form):
#        remember_me = form.cleaned_data['remember_me']
#        login(self.request, form.get_user())
#        if remember_me:
#            self.request.session.set_expiry(1209600)
#        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse('main:index', args=(self.request.user.id, ))


class UserLogoutView(LogoutView):
    next_page = '/'
