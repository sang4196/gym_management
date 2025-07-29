from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardWidgetViewSet,
    DashboardLayoutViewSet,
    UserDashboardViewSet,
    UserDashboardWidgetViewSet,
    ReportViewSet,
    ReportExecutionViewSet,
    dashboard_overview,
    revenue_chart,
    member_stats,
    trainer_stats,
    reservation_stats,
    branch_comparison
)

app_name = 'dashboards'

router = DefaultRouter()
router.register(r'widgets', DashboardWidgetViewSet)
router.register(r'layouts', DashboardLayoutViewSet)
router.register(r'user-dashboards', UserDashboardViewSet)
router.register(r'user-dashboard-widgets', UserDashboardWidgetViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'report-executions', ReportExecutionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('overview/', dashboard_overview, name='dashboard-overview'),
    path('revenue-chart/', revenue_chart, name='revenue-chart'),
    path('member-stats/', member_stats, name='member-stats'),
    path('trainer-stats/', trainer_stats, name='trainer-stats'),
    path('reservation-stats/', reservation_stats, name='reservation-stats'),
    path('branch-comparison/', branch_comparison, name='branch-comparison'),
]
