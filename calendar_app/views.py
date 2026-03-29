from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Event


def get_events(request):
    events = Event.objects.select_related(
        "_sport", "_home_team", "_away_team", "_venue"
    ).all()

    data = []
    for event in events:
        data.append({
            "id": event.id,
            "title": event.title,
            "date": event.event_date.isoformat(),
            "time": event.event_time.isoformat(),
            "sport": event._sport.name,
            "home_team": event._home_team.name,
            "away_team": event._away_team.name,
            "venue": event._venue.name if event._venue else None,
            "description": event.description,
        })

    return JsonResponse(data, safe=False)


def get_event(request, event_id):
    event = get_object_or_404(
        Event.objects.select_related(
            "_sport", "_home_team", "_away_team", "_venue"
        ),
        id=event_id
    )

    data = {
        "id": event.id,
        "title": event.title,
        "date": event.event_date.isoformat(),
        "time": event.event_time.isoformat(),
        "sport": event._sport.name,
        "home_team": event._home_team.name,
        "away_team": event._away_team.name,
        "venue": event._venue.name if event._venue else None,
        "description": event.description,
    }

    return JsonResponse(data)
