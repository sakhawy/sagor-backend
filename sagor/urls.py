from django.urls import path, include
from rest_framework import routers

from sagor import views

router = routers.DefaultRouter()
router.register(r'farms', views.FarmViewSet)
router.register(r'gateways', views.GatewayViewSet)
router.register(r'tanks', views.TankViewSet)
router.register(r'packages', views.PackageViewSet)
router.register(r'ph_sensor_readings', views.PHSensorReadingViewSet)
router.register(r'temprature_sensor_readings', views.TempratureSensorReadingViewSet)
router.register(r'camera_sensor_readings', views.CameraSensorReadingViewSet)
router.register(r'pumped_food', views.PumpedFoodViewSet)
router.register(r'pumps', views.PumpViewSet)

urlpatterns = [
    path('', include(router.urls))
]
