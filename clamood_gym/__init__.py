# Clamood Gym Management System

# Celery 앱을 Django 앱이 시작될 때 로드
from .celery import app as celery_app

__all__ = ('celery_app',) 