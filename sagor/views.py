from rest_framework.viewsets import ReadOnlyModelViewSet

from sagor import models
from sagor import serializers


class FarmViewSet(ReadOnlyModelViewSet):
    queryset = models.Farm.objects.all()
    serializer_class = serializers.FarmSerializer


class GatewayViewSet(ReadOnlyModelViewSet):
    queryset = models.Gateway.objects.all()
    serializer_class = serializers.GatewaySerializer


class TankViewSet(ReadOnlyModelViewSet):
    queryset = models.Tank.objects.all()
    serializer_class = serializers.TankSerializer


class PackageViewSet(ReadOnlyModelViewSet):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer


class PHSensorReadingViewSet(ReadOnlyModelViewSet):
    queryset = models.PHSensorReading.objects.all()
    serializer_class = serializers.PHSensorReadingSerializer


class TempratureSensorReadingViewSet(ReadOnlyModelViewSet):
    queryset = models.TempratureSensorReading.objects.all()
    serializer_class = serializers.TempratureSensorReadingSerializer


class CameraSensorReadingViewSet(ReadOnlyModelViewSet):
    queryset = models.CameraSensorReading.objects.all()
    serializer_class = serializers.CameraSensorReadingSerializer
