from django.conf.urls import include, handler400,handler403,handler404, handler500
from django.urls import path
from django.contrib import admin


urlpatterns = [
    path('user/', include('userControl.urls')),
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path('', include('dashboard.urls')),
]

handler400 = 'dashboard.views.error400'
handler403 = 'dashboard.views.error403'
handler404 = 'dashboard.views.error404'
handler404 = 'dashboard.views.error500'



