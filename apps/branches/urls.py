from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BranchViewSet, BranchAdminViewSet

app_name = 'branches'

router = DefaultRouter()
router.register(r'branches', BranchViewSet)
router.register(r'admins', BranchAdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
