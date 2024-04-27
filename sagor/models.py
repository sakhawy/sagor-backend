from django.db import models

class Farm(models.Model):
    name = models.CharField(max_length=250)


class Gateway(models.Model):
    class Status(models.TextChoices):
        OK = 'OK', 'Ok'
        ERROR = 'ERROR', 'Error'


    broker_url = models.URLField()
    ip = models.IPAddressField()
    status = models.CharField(
        max_length = 250,
        choices=Status.choices,
        default=Status.OK,
    )
    mac_address = models.CharField(max_length=250)

    farm = models.ForeignKey(
        'Farm',
        on_delete=models.CASCADE,
        related_name='gateways',
    )


class Tanks(models.Model):
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
        # consider changing to PROTECT
        on_delete=models.SET_NULL,
        related_name='tanks',
    )


class Package(models.Model):
    class Status(models.TextChoices):
        OK = 'OK', 'Ok'
        ERROR = 'ERROR', 'Error'


    status = models.CharField(
        max_length=250,
        choices=Status.choices,
        default=Status.OK
    )
    last_checked_at = models.DateTimeField()

    tank = models.ForeignKey(
        'Package',
        on_delete=models.SET_NULL,
        related_name='packages',
    )

class Pump(models.Model):
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


class PumpedFood(models.Model):
    class Status(models.TextChoices):
        OK = 'OK', 'Ok'
        ERROR = 'ERROR', 'Error'

    
    quantity = models.DecimalField()
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


class BaseSensor(models.Model):
    class ReadingStatus(models.TextChoices):
        SANE = 'SANE', 'Sane'
        NOT_SANE = 'NOT_SANE', 'Not sane'


    reading_status = models.CharField(
        max_length=250,
        choices=ReadingStatus.choices,
        default=ReadingStatus.SANE,
    )
    run_every = models.DecimalField()

    package = models.ForeignKey(
        'Package',
        on_delete=models.CASCADE,
        related_name='sensors'
    )

class PHSensor(BaseSensor):
    value = models.DecimalField()


class TempratureSensor(BaseSensor):
    value = models.DecimalField()


class CameraSensor(BaseSensor):
    value = models.BinaryField()


