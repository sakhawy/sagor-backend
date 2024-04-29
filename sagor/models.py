import uuid

from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created on')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updated')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Deleted on')

    class Meta:
        abstract = True


def _generate_farm_name():
        return uuid.uuid4()


class Farm(TimeStampedModel):
    name = models.CharField(
        max_length=250,
        default=_generate_farm_name
    )


class Gateway(TimeStampedModel):
    class Status(models.TextChoices):
        OK = 'OK', 'Ok'
        ERROR = 'ERROR', 'Error'


    broker_url = models.URLField(
        null=True, 
        blank=True
    )
    ip = models.GenericIPAddressField(
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length = 250,
        choices=Status.choices,
        default=Status.OK,
    )
    mac_address = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    farm = models.ForeignKey(
        'Farm',
        on_delete=models.CASCADE,
        related_name='gateways',
    )


class Tank(TimeStampedModel):
    class FishType(models.TextChoices):
        TILAPIA = 'TILAPIA', 'Tilapia'
    

    class Status(models.TextChoices):
        '''
        You have to think before extending this enum.
        For example, a tank can have overfed fish AND
        unhealthy water. There are a lot of indep statuses.
        '''
        HEALTHY = 'HEALTHY', 'Healthy'
        UNHEALTHY = 'UNHEALTHY', 'Unhealthy'


    fish_type = models.CharField(
        max_length=250,
        choices=FishType.choices,
        default=FishType.TILAPIA,
    )
    status = models.CharField(
        max_length=250,
        choices=Status.choices,
        default=Status.HEALTHY,
    )

    gateway = models.ForeignKey(
        'Gateway',
        on_delete=models.PROTECT,
        related_name='tanks',
    )


class Package(TimeStampedModel):
    class Status(models.TextChoices):
        OK = 'OK', 'Ok'
        ERROR = 'ERROR', 'Error'


    status = models.CharField(
        max_length=250,
        choices=Status.choices,
        default=Status.OK
    )
    last_checked_at = models.DateTimeField(auto_now=True, verbose_name='Last checked at')

    tank = models.ForeignKey(
        'Tank',
        on_delete=models.PROTECT,
        related_name='packages',
    )

class Pump(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive',
        ERROR = 'ERROR', 'Error'


    status = models.CharField(
        max_length=250,
        choices=Status.choices,
        default=Status.INACTIVE
    )

    tank = models.ForeignKey(
        'Tank',
        on_delete=models.CASCADE,
        related_name='pumps',
    )


class PumpedFood(TimeStampedModel):
    class Status(models.TextChoices):
        OK = 'OK', 'Ok'
        ERROR = 'ERROR', 'Error'

    
    quantity = models.DecimalField(decimal_places=4, max_digits=10)
    status = models.CharField(
        max_length=250,
        choices=Status.choices,
        default=Status.OK
    )

    pump = models.ForeignKey(
        'Pump',
        on_delete=models.CASCADE,
        related_name='pumped_food',
    )


class BaseSensorReading(TimeStampedModel):
    class Meta:
        abstract = True


    class ReadingStatus(models.TextChoices):
        SANE = 'SANE', 'Sane'
        NOT_SANE = 'NOT_SANE', 'Not sane'


    reading_status = models.CharField(
        max_length=250,
        choices=ReadingStatus.choices,
        default=ReadingStatus.SANE,
    )
    
    # in milliseconds
    read_every = models.IntegerField(default=1000)


class PHSensorReading(BaseSensorReading):
    value = models.DecimalField(decimal_places=10, max_digits=10)
    package = models.ForeignKey(
        'Package',
        on_delete=models.CASCADE,
        related_name='ph_sensor_readings'
    )

class TempratureSensorReading(BaseSensorReading):
    value = models.DecimalField(decimal_places=10, max_digits=10)
    package = models.ForeignKey(
        'Package',
        on_delete=models.CASCADE,
        related_name='temprature_sensor_readings'
    )

class CameraSensorReading(BaseSensorReading):
    value = models.BinaryField()
    package = models.ForeignKey(
        'Package',
        on_delete=models.CASCADE,
        related_name='camera_sensor_readings'
    )

