from Versionize import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from user.views import UserLoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UserLoginView.as_view(), name='login'),
    path('user/', include('user.urls', namespace='user')),
    path('main/', include('main.urls', namespace='main')),
    path('admins/', include('admins.urls', namespace='admins')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
