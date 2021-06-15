from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name='join'),
    path('signin/',views.signin,name='login'),
    path('logout/',views.logout,name='logout'),

]
