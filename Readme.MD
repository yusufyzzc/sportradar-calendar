# Sportradar Calendar App

A small Django app for tracking sports events.

- A web UI to list events, inspect details and add new events
- JSON API endpoints for listing, viewing and creating events
- A simple SQLite database setup for local development

## Features
- View all events
- View event details
- Create events (API + UI)

## Tech Stack
- Python
- Django
- SQLite

## Setup

```bash
git clone https://github.com/yusufyzzc/sportradar-calendar.git

cd sportradar-calendar

python -m venv venv

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
