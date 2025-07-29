from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReservationViewSet,
    PTRecordViewSet,
    PTRecordImageViewSet,
    ReservationChangeLogViewSet
)

app_name = 'reservations'

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet)
router.register(r'pt-records', PTRecordViewSet)
router.register(r'pt-record-images', PTRecordImageViewSet)
router.register(r'change-logs', ReservationChangeLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
