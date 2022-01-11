from django.http import HttpResponseRedirect


from django.urls import reverse
from admins.forms import UserRegistrationFrom


def index(request):
    return render(request, 'admins/admin.html')



def admins_users_create(request):
    return render(request, 'admins/admin-users-create.html')

def admins_users_create(request):
    if request.method == 'POST':
        form = UserRegistrationFrom(data=request.POST, files=request.FILES)
        form.save()
        return HttpResponseRedirect(reverse('admins:index'))
    else:
        form = UserRegistrationFrom()
    context = {'title': 'Create user',
               'form': form}
    return render(request, 'admins/admin-users-create.html', context)
from django.shortcuts import render
