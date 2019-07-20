from django.urls import path
from . import views

urlpatterns = [
    path('', views.eventList, name='index'),
    path('events/new', views.new_event_form, name='event-new'),
    path('events/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/edit', views.edit_event_form, name='event-edit'),
    path('events/<int:pk>/delete', views.delete_event, name='event-delete'),
]