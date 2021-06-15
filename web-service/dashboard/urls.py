from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('init/',views.init, name='init'),
    path('server/',views.apiCreateServer,name='create'),
    path('search/',views.search,name='search'),
    path('detail/',views.detail,name='detail'),
    path('chat/<str:room_name>/', views.room, name='room'),
]





