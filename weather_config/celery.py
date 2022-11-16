from celery import Celery
from celery.schedules import crontab
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_config.settings")

app = Celery("weather_config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "parse_weather-every-day 9 AM": {
        "task": "main.tasks.parse_beat_weather",
        "schedule": crontab(hour='9', minute=0)
    }
}
