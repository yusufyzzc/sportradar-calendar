from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Event, Sport, Team, Venue
import json

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

def event_list_page(request):
    events = Event.objects.select_related(
        "_sport", "_home_team", "_away_team", "_venue"
    ).all().order_by("event_date", "event_time")

    return render(request, "calendar_app/event_list.html", {"events": events})


def event_detail_page(request, event_id):
    event = get_object_or_404(
        Event.objects.select_related(
            "_sport", "_home_team", "_away_team", "_venue"
        ),
        id=event_id
    )

    return render(request, "calendar_app/event_detail.html", {"event": event})


def add_event_page(request):
    if request.method == "POST":
        sport = Sport.objects.get(id=request.POST["sport_id"])
        home_team = Team.objects.get(id=request.POST["home_team_id"])
        away_team = Team.objects.get(id=request.POST["away_team_id"])

        venue = None
        venue_id = request.POST.get("venue_id")
        if venue_id:
            venue = Venue.objects.get(id=venue_id)

        Event.objects.create(
            title=request.POST.get("title", ""),
            event_date=request.POST["event_date"],
            event_time=request.POST["event_time"],
            description=request.POST.get("description", ""),
            _sport=sport,
            _home_team=home_team,
            _away_team=away_team,
            _venue=venue,
        )

        return redirect("event_list_page")

    context = {
        "sports": Sport.objects.all(),
        "teams": Team.objects.all(),
        "venues": Venue.objects.all(),
    }
    return render(request, "calendar_app/event_form.html", context)
