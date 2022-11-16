from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.tasks import parse_weather
from main.serializers import WeatherSerializer
from main.models import Weather
from weather_config.celery import app


class WeatherView(APIView):
    # def post(self, request):
    #     """
    #     Реализовать через ендпоинт изменение времени обновления информации о погоде.
    #     """
    #     try:
    #         new_time = request.data['new_time']
    #         return Response({f"Task time successfully changed: {new_time}"}, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         print(e)
    #         return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """
        Реализовать ендпоинт для получения информации о погоде через Django Rest Framework.
        """
        data = parse_weather()
        serializer = WeatherSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetWeatherWithTask(APIView):
    def post(self, request):
        """
            Реализовать через ендпоинт ручное обновление (запуск таски) информации о погоде:
        """
        data = parse_weather.delay()
        return Response({"task_id": data.id, "status": data.status}, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
            Дать возможность отслеживать статус задачи парсинга (Scheduled, In Progress, Done)
        """
        action = request.data['task_id']
        res = AsyncResult(action, app=app)
        return Response({"status": res.state, "response": res.get()}, status=status.HTTP_200_OK)
