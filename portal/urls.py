from django.urls import path
from . import views

urlpatterns = [
    path('', views.eventList, name='index'),
    path('newevent', views.new_event_form, name='newevent'),
]