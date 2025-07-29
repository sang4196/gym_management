"""
URL configuration for clamood_gym project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.branches.views import CustomAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth URLs - 직접 정의
    path('api/auth/login/', CustomAuthToken.as_view(), name='auth_login'),
    # API URLs
    path('api/branches/', include('apps.branches.urls')),
    path('api/members/', include('apps.members.urls')),
    path('api/trainers/', include('apps.trainers.urls')),
    path('api/reservations/', include('apps.reservations.urls')),
    path('api/salaries/', include('apps.salaries.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/dashboards/', include('apps.dashboards.urls')),
]

# 개발 환경에서 정적 파일과 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT) 