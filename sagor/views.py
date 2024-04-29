from rest_framework.viewsets import ModelViewSet

from sagor import models
from sagor import serializers


class FarmViewSet(ModelViewSet):
    queryset = models.Farm.objects.all()
    serializer_class = serializers.FarmSerializer


class GatewayViewSet(ModelViewSet):
    queryset = models.Gateway.objects.all()
    serializer_class = serializers.GatewaySerializer


class TankViewSet(ModelViewSet):
    queryset = models.Tank.objects.all()
    serializer_class = serializers.TankSerializer


class PackageViewSet(ModelViewSet):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer


class PHSensorReadingViewSet(ModelViewSet):
    queryset = models.PHSensorReading.objects.all()
    serializer_class = serializers.PHSensorReadingSerializer


class TempratureSensorReadingViewSet(ModelViewSet):
    queryset = models.TempratureSensorReading.objects.all()
    serializer_class = serializers.TempratureSensorReadingSerializer


class CameraSensorReadingViewSet(ModelViewSet):
    queryset = models.CameraSensorReading.objects.all()
    serializer_class = serializers.CameraSensorReadingSerializer
