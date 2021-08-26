from django.urls import path
from .views import usergame_list
from .views import userevent_list

urlpatterns = [
    path('reports/usergames', usergame_list),
]

urlpatterns = [
    path('reports/userevents', userevent_list),
]
