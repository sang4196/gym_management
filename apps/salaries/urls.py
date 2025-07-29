from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SalaryViewSet,
    IncentiveDetailViewSet,
    AdditionalRevenueViewSet,
    OtherCostViewSet,
    BranchRevenueViewSet
)

app_name = 'salaries'

router = DefaultRouter()
router.register(r'salaries', SalaryViewSet)
router.register(r'incentive-details', IncentiveDetailViewSet)
router.register(r'additional-revenues', AdditionalRevenueViewSet)
router.register(r'other-costs', OtherCostViewSet)
router.register(r'branch-revenues', BranchRevenueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
