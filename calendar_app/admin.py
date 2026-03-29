from django.contrib import admin
from .models import Sport, Team, Venue, Event

admin.site.register(Sport)
admin.site.register(Team)
admin.site.register(Venue)
admin.site.register(Event)