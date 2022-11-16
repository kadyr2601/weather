from weather_config.celery import app
from main.service import parser


@app.task
def parse_weather():
    res = parser()
    return res


@app.task
def parse_beat_weather() -> None:
    parser()
