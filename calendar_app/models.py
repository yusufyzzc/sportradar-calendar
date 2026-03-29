from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=150)
    country_code = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200, blank=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    description = models.TextField(blank=True, null=True)

    _sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        related_name="events"
    )
    _home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="home_events"
    )
    _away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_events"
    )
    _venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.title:
            return self.title
        return f"{self._home_team} vs {self._away_team} - {self.event_date}"

    @property
    def sport(self):
        return self._sport

    @property
    def home_team(self):
        return self._home_team

    @property
    def away_team(self):
        return self._away_team

    @property
    def venue(self):
        return self._venue
