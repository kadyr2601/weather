from django.contrib import admin
from main.models import Weather


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ['date', 'temperature', 'weather_description']
    search_fields = ['date', ]
