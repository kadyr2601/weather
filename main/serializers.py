from rest_framework import serializers
from main.models import Weather


class WeatherSerializer(serializers.Serializer):
    date = serializers.DateField()
    temperature = serializers.CharField(max_length=8)
    weather_description = serializers.CharField(max_length=128)

    # def to_representation(self, instance):
    #     representation = super(WeatherSerializer, self).to_representation(instance)
    #     representation['date'] = instance.date.strftime('%d-%m-%Y')
    #     return representation
