from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Event
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Sport, Team, Venue


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


@csrf_exempt
def create_event(request):
    if request.method == "POST":
        body = json.loads(request.body)

        sport = Sport.objects.get(id=body["sport_id"])
        home_team = Team.objects.get(id=body["home_team_id"])
        away_team = Team.objects.get(id=body["away_team_id"])

        venue = None
        if "venue_id" in body:
            venue = Venue.objects.get(id=body["venue_id"])

        event = Event.objects.create(
            title=body.get("title", ""),
            event_date=body["date"],
            event_time=body["time"],
            _sport=sport,
            _home_team=home_team,
            _away_team=away_team,
            _venue=venue,
        )

        return JsonResponse({"message": "Event created", "id": event.id})

    return JsonResponse({"error": "Invalid request"}, status=400)
