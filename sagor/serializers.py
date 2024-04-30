from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from sagor import models


class PHSensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PHSensorReading
        fields = (
            'id',
            'created_at',
            'updated_at',
            'reading_status',
            'read_every',
            'value',
        )


class TempratureSensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TempratureSensorReading
        fields = (
            'id',
            'created_at',
            'updated_at',
            'reading_status',
            'read_every',
            'value',
        )


class CameraSensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CameraSensorReading
        fields = (
            'id',
            'created_at',
            'updated_at',
            'reading_status',
            'read_every',
            'value',
        )


class PackageSerializer(WritableNestedModelSerializer):
    ph_sensor_readings = PHSensorReadingSerializer(many=True)
    temprature_sensor_readings = TempratureSensorReadingSerializer(many=True)
    camera_sensor_readings = CameraSensorReadingSerializer(many=True)

    class Meta:
        model = models.Package
        fields = (
            'id',
            'status',
            'last_checked_at',
            'ph_sensor_readings',
            'temprature_sensor_readings',
            'camera_sensor_readings',
        )


class TankSerializer(WritableNestedModelSerializer):
    packages = PackageSerializer(many=True)

    class Meta:
        model = models.Tank
        fields = (
            'id',
            'fish_type',
            'status',
            'packages',
        )


class GatewaySerializer(WritableNestedModelSerializer):
    tanks = TankSerializer(many=True)

    class Meta:
        model = models.Gateway
        fields = (
            'id',
            'broker_url',
            'ip',
            'status',
            'mac_address',
            'tanks',
        )


class FarmSerializer(WritableNestedModelSerializer):
    gateways = GatewaySerializer(many=True)

    class Meta:
        model = models.Farm
        fields = (
            'id',
            'created_at',
            'updated_at',
            'name',
            'gateways'
        )

class IoTDataSerializer(serializers.Serializer):
    farm = FarmSerializer(many=False)

    def create(self, validated_data):
        farm_serializer = FarmSerializer(data=validated_data['farm'])
        if farm_serializer.is_valid(raise_exception=True):
            return farm_serializer.save()
