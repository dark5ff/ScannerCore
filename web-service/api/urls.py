from django.urls import path
from . import views, graph_views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkEngine/',views.checkEngine),
    path('checkKeyword/',views.checkKeyword),
    path('showDetect/',views.showDetect),
    path('graph/main',graph_views.mainGraph),
    path('graph/blue',graph_views.stickGraph),


]





