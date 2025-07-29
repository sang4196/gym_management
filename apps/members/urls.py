from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, PTProgramViewSet, MemberPTRegistrationViewSet

app_name = 'members'

router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'pt-programs', PTProgramViewSet)
router.register(r'pt-registrations', MemberPTRegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
