from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NotificationViewSet,
    NotificationTemplateViewSet,
    NotificationLogViewSet
)

app_name = 'notifications'

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)
router.register(r'templates', NotificationTemplateViewSet)
router.register(r'logs', NotificationLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
