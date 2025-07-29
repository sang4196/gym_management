from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TrainerViewSet,
    TrainerIncentiveViewSet,
    TrainerScheduleViewSet,
    TrainerBlockedTimeViewSet
)

app_name = 'trainers'

router = DefaultRouter()
router.register(r'trainers', TrainerViewSet)
router.register(r'incentives', TrainerIncentiveViewSet)
router.register(r'schedules', TrainerScheduleViewSet)
router.register(r'blocked-times', TrainerBlockedTimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
