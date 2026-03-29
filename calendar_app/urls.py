from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_list_page, name="event_list_page"),
    path("events/", views.get_events, name="get_events"),
    path("events/<int:event_id>/", views.get_event, name="get_event"),
    path("events/create/", views.create_event, name="create_event"),
    path("events/page/<int:event_id>/", views.event_detail_page, name="event_detail_page"),
    path("events/add/", views.add_event_page, name="add_event_page"),
]