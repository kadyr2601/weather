from django.urls import path
from main.views import WeatherView, GetWeatherWithTask

urlpatterns = [
    path('', WeatherView.as_view()),
    path('check-weather/', GetWeatherWithTask.as_view())
]
