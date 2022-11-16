from django.db import models


class Weather(models.Model):
    date = models.DateField()
    temperature = models.CharField(max_length=8)
    weather_description = models.CharField(max_length=128)
