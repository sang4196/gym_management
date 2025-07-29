from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncDate, TruncMonth
from apps.branches.models import Branch
from apps.members.models import Member, MemberPTRegistration
from apps.trainers.models import Trainer
from apps.reservations.models import Reservation, PTRecord
from apps.salaries.models import Salary, BranchRevenue


class DashboardService:
    """대시보드 서비스"""
    
    def __init__(self):
        pass
    
    def get_overview_statistics(self, branch_id: Optional[int] = None) -> Dict[str, Any]:
        """전체 통계 개요"""
        queryset_filters = {}
        if branch_id:
            queryset_filters['branch_id'] = branch_id
        
        # 회원 통계
        total_members = Member.objects.filter(**queryset_filters, membership_status='active').count()
        new_members_this_month = Member.objects.filter(
            **queryset_filters,
            registration_date__month=datetime.now().month,
            registration_date__year=datetime.now().year
        ).count()
        
        # 트레이너 통계
        total_trainers = Trainer.objects.filter(**queryset_filters, employment_status='active').count()
        
        # 예약 통계
        today = date.today()
        today_reservations = Reservation.objects.filter(
            **queryset_filters,
            date=today,
            reservation_status='confirmed'
        ).count()
        
        # 매출 통계 (이번 달)
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        if branch_id:
            monthly_revenue = BranchRevenue.objects.filter(
                branch_id=branch_id,
                year=current_year,
                month=current_month
            ).first()
            monthly_revenue_amount = monthly_revenue.total_revenue if monthly_revenue else 0
        else:
            monthly_revenue_amount = BranchRevenue.objects.filter(
                year=current_year,
                month=current_month
            ).aggregate(total=Sum('total_revenue'))['total'] or 0
        
        return {
            'total_members': total_members,
            'new_members_this_month': new_members_this_month,
            'total_trainers': total_trainers,
            'today_reservations': today_reservations,
            'monthly_revenue': monthly_revenue_amount,
        }
    
    def get_weekly_statistics(self, branch_id: Optional[int] = None, 
                            start_date: Optional[date] = None, 
                            end_date: Optional[date] = None) -> Dict[str, Any]:
        """주간 통계"""
        if not start_date:
            start_date = date.today() - timedelta(days=7)
        if not end_date:
            end_date = date.today()
        
        queryset_filters = {}
        if branch_id:
            queryset_filters['branch_id'] = branch_id
        
        # 신규 회원
        new_members = Member.objects.filter(
            **queryset_filters,
            registration_date__range=[start_date, end_date]
        ).count()
        
        # PT 예약
        total_reservations = Reservation.objects.filter(
            **queryset_filters,
            date__range=[start_date, end_date]
        ).count()
        
        completed_reservations = Reservation.objects.filter(
            **queryset_filters,
            date__range=[start_date, end_date],
            reservation_status='completed'
        ).count()
        
        # 매출
        if branch_id:
            revenues = BranchRevenue.objects.filter(
                branch_id=branch_id,
                year__gte=start_date.year,
                year__lte=end_date.year
            )
            if start_date.year == end_date.year:
                revenues = revenues.filter(month__gte=start_date.month, month__lte=end_date.month)
            total_revenue = revenues.aggregate(total=Sum('total_revenue'))['total'] or 0
        else:
            total_revenue = 0  # 전체 지점의 경우 복잡한 계산 필요
        
        return {
            'new_members': new_members,
            'total_reservations': total_reservations,
            'completed_reservations': completed_reservations,
            'total_revenue': total_revenue,
            'completion_rate': (completed_reservations / total_reservations * 100) if total_reservations > 0 else 0
        }
    
    def get_monthly_statistics(self, year: int, month: int, 
                             branch_id: Optional[int] = None) -> Dict[str, Any]:
        """월간 통계"""
        queryset_filters = {}
        if branch_id:
            queryset_filters['branch_id'] = branch_id
        
        # 회원 통계
        total_members = Member.objects.filter(**queryset_filters, membership_status='active').count()
        new_members = Member.objects.filter(
            **queryset_filters,
            registration_date__year=year,
            registration_date__month=month
        ).count()
        
        # PT 등록 통계
        pt_registrations = MemberPTRegistration.objects.filter(
            **queryset_filters,
            registration_date__year=year,
            registration_date__month=month
        )
        total_pt_registrations = pt_registrations.count()
        total_pt_revenue = pt_registrations.aggregate(total=Sum('total_price'))['total'] or 0
        
        # 예약 통계
        reservations = Reservation.objects.filter(
            **queryset_filters,
            date__year=year,
            date__month=month
        )
        total_reservations = reservations.count()
        completed_reservations = reservations.filter(reservation_status='completed').count()
        
        # 매출 통계
        if branch_id:
            monthly_revenue = BranchRevenue.objects.filter(
                branch_id=branch_id,
                year=year,
                month=month
            ).first()
            total_revenue = monthly_revenue.total_revenue if monthly_revenue else 0
        else:
            total_revenue = BranchRevenue.objects.filter(
                year=year,
                month=month
            ).aggregate(total=Sum('total_revenue'))['total'] or 0
        
        return {
            'total_members': total_members,
            'new_members': new_members,
            'total_pt_registrations': total_pt_registrations,
            'total_pt_revenue': total_pt_revenue,
            'total_reservations': total_reservations,
            'completed_reservations': completed_reservations,
            'total_revenue': total_revenue,
            'completion_rate': (completed_reservations / total_reservations * 100) if total_reservations > 0 else 0
        }
    
    def get_revenue_chart_data(self, branch_id: Optional[int] = None, 
                             months: int = 12) -> Dict[str, Any]:
        """매출 차트 데이터"""
        end_date = date.today()
        start_date = end_date - timedelta(days=months * 30)
        
        queryset_filters = {}
        if branch_id:
            queryset_filters['branch_id'] = branch_id
        
        # 월별 매출 데이터
        revenues = BranchRevenue.objects.filter(
            **queryset_filters,
            year__gte=start_date.year,
            year__lte=end_date.year
        ).order_by('year', 'month')
        
        labels = []
        data = []
        
        for revenue in revenues:
            labels.append(f"{revenue.year}년 {revenue.month}월")
            data.append(float(revenue.total_revenue))
        
        return {
            'labels': labels,
            'data': data,
            'type': 'line'
        }
    
    def get_reservation_chart_data(self, branch_id: Optional[int] = None, 
                                 days: int = 30) -> Dict[str, Any]:
        """예약 차트 데이터"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        queryset_filters = {}
        if branch_id:
            queryset_filters['branch_id'] = branch_id
        
        # 일별 예약 데이터
        reservations = Reservation.objects.filter(
            **queryset_filters,
            date__range=[start_date, end_date]
        ).annotate(
            day=TruncDate('date')
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        labels = []
        data = []
        
        for item in reservations:
            labels.append(item['day'].strftime('%m/%d'))
            data.append(item['count'])
        
        return {
            'labels': labels,
            'data': data,
            'type': 'bar'
        }
    
    def get_member_growth_data(self, branch_id: Optional[int] = None, 
                             months: int = 12) -> Dict[str, Any]:
        """회원 증가 데이터"""
        end_date = date.today()
        start_date = end_date - timedelta(days=months * 30)
        
        queryset_filters = {}
        if branch_id:
            queryset_filters['branch_id'] = branch_id
        
        # 월별 신규 회원 데이터
        new_members = Member.objects.filter(
            **queryset_filters,
            registration_date__range=[start_date, end_date]
        ).annotate(
            month=TruncMonth('registration_date')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        labels = []
        data = []
        
        for item in new_members:
            labels.append(item['month'].strftime('%Y년 %m월'))
            data.append(item['count'])
        
        return {
            'labels': labels,
            'data': data,
            'type': 'line'
        }
    
    def get_trainer_performance_data(self, branch_id: Optional[int] = None, 
                                   month: Optional[int] = None, 
                                   year: Optional[int] = None) -> List[Dict[str, Any]]:
        """트레이너 성과 데이터"""
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
        
        queryset_filters = {}
        if branch_id:
            queryset_filters['branch_id'] = branch_id
        
        trainers = Trainer.objects.filter(**queryset_filters, employment_status='active')
        
        performance_data = []
        
        for trainer in trainers:
            # 완료된 PT 세션 수
            completed_sessions = PTRecord.objects.filter(
                trainer=trainer,
                workout_date__year=year,
                workout_date__month=month,
                is_completed=True
            ).count()
            
            # 총 예약 수
            total_reservations = Reservation.objects.filter(
                trainer=trainer,
                date__year=year,
                date__month=month
            ).count()
            
            # 완료율
            completion_rate = (completed_sessions / total_reservations * 100) if total_reservations > 0 else 0
            
            # 급여
            salary = Salary.objects.filter(
                trainer=trainer,
                year=year,
                month=month
            ).first()
            
            performance_data.append({
                'trainer_name': trainer.name,
                'completed_sessions': completed_sessions,
                'total_reservations': total_reservations,
                'completion_rate': round(completion_rate, 1),
                'salary': float(salary.total_salary) if salary else 0
            })
        
        return performance_data
    
    def get_branch_comparison_data(self, year: int, month: int) -> List[Dict[str, Any]]:
        """지점별 비교 데이터"""
        branches = Branch.objects.filter(is_active=True)
        
        comparison_data = []
        
        for branch in branches:
            # 회원 수
            total_members = Member.objects.filter(
                branch=branch,
                membership_status='active'
            ).count()
            
            # 신규 회원
            new_members = Member.objects.filter(
                branch=branch,
                registration_date__year=year,
                registration_date__month=month
            ).count()
            
            # 매출
            revenue = BranchRevenue.objects.filter(
                branch=branch,
                year=year,
                month=month
            ).first()
            total_revenue = revenue.total_revenue if revenue else 0
            
            # 예약 수
            total_reservations = Reservation.objects.filter(
                Q(member__branch=branch) | Q(trainer__branch=branch),
                date__year=year,
                date__month=month
            ).count()
            
            comparison_data.append({
                'branch_name': branch.name,
                'total_members': total_members,
                'new_members': new_members,
                'total_revenue': float(total_revenue),
                'total_reservations': total_reservations
            })
        
        return comparison_data
    
    def get_dashboard_widgets(self, user_type: str, user_id: int) -> List[Dict[str, Any]]:
        """사용자별 대시보드 위젯"""
        from .models import UserDashboard, DashboardWidget
        
        try:
            user_dashboard = UserDashboard.objects.get(
                user_type=user_type,
                user_id=user_id
            )
            
            widgets = []
            for user_widget in user_dashboard.userdashboardwidget_set.filter(is_visible=True):
                widget_data = {
                    'id': user_widget.widget.id,
                    'name': user_widget.widget.name,
                    'title': user_widget.widget.title,
                    'widget_type': user_widget.widget.widget_type,
                    'chart_type': user_widget.widget.chart_type,
                    'position_x': user_widget.position_x,
                    'position_y': user_widget.position_y,
                    'width': user_widget.width,
                    'height': user_widget.height,
                    'config': user_widget.config
                }
                
                # 위젯 데이터 생성
                if user_widget.widget.widget_type == 'revenue_chart':
                    widget_data['data'] = self.get_revenue_chart_data()
                elif user_widget.widget.widget_type == 'member_stats':
                    widget_data['data'] = self.get_overview_statistics()
                elif user_widget.widget.widget_type == 'reservation_stats':
                    widget_data['data'] = self.get_reservation_chart_data()
                
                widgets.append(widget_data)
            
            return widgets
            
        except UserDashboard.DoesNotExist:
            # 기본 위젯 반환
            return self.get_default_widgets()
    
    def get_default_widgets(self) -> List[Dict[str, Any]]:
        """기본 위젯"""
        return [
            {
                'id': 1,
                'name': 'overview_stats',
                'title': '전체 통계',
                'widget_type': 'metric_card',
                'position_x': 0,
                'position_y': 0,
                'width': 12,
                'height': 2,
                'data': self.get_overview_statistics()
            },
            {
                'id': 2,
                'name': 'revenue_chart',
                'title': '매출 추이',
                'widget_type': 'revenue_chart',
                'chart_type': 'line',
                'position_x': 0,
                'position_y': 2,
                'width': 6,
                'height': 4,
                'data': self.get_revenue_chart_data()
            },
            {
                'id': 3,
                'name': 'reservation_chart',
                'title': '예약 현황',
                'widget_type': 'reservation_stats',
                'chart_type': 'bar',
                'position_x': 6,
                'position_y': 2,
                'width': 6,
                'height': 4,
                'data': self.get_reservation_chart_data()
            }
        ]
    
    def generate_report(self, report_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """리포트 생성"""
        if report_type == 'revenue':
            return self._generate_revenue_report(parameters)
        elif report_type == 'member':
            return self._generate_member_report(parameters)
        elif report_type == 'trainer':
            return self._generate_trainer_report(parameters)
        elif report_type == 'reservation':
            return self._generate_reservation_report(parameters)
        else:
            return {'error': '지원하지 않는 리포트 유형입니다.'}
    
    def _generate_revenue_report(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """매출 리포트 생성"""
        year = parameters.get('year', datetime.now().year)
        month = parameters.get('month', datetime.now().month)
        branch_id = parameters.get('branch_id')
        
        monthly_stats = self.get_monthly_statistics(year, month, branch_id)
        revenue_chart = self.get_revenue_chart_data(branch_id)
        
        return {
            'type': 'revenue',
            'period': f"{year}년 {month}월",
            'summary': monthly_stats,
            'chart_data': revenue_chart,
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_member_report(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """회원 리포트 생성"""
        year = parameters.get('year', datetime.now().year)
        month = parameters.get('month', datetime.now().month)
        branch_id = parameters.get('branch_id')
        
        monthly_stats = self.get_monthly_statistics(year, month, branch_id)
        member_growth = self.get_member_growth_data(branch_id)
        
        return {
            'type': 'member',
            'period': f"{year}년 {month}월",
            'summary': monthly_stats,
            'chart_data': member_growth,
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_trainer_report(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """트레이너 리포트 생성"""
        year = parameters.get('year', datetime.now().year)
        month = parameters.get('month', datetime.now().month)
        branch_id = parameters.get('branch_id')
        
        performance_data = self.get_trainer_performance_data(branch_id, month, year)
        
        return {
            'type': 'trainer',
            'period': f"{year}년 {month}월",
            'performance_data': performance_data,
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_reservation_report(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """예약 리포트 생성"""
        year = parameters.get('year', datetime.now().year)
        month = parameters.get('month', datetime.now().month)
        branch_id = parameters.get('branch_id')
        
        monthly_stats = self.get_monthly_statistics(year, month, branch_id)
        reservation_chart = self.get_reservation_chart_data(branch_id)
        
        return {
            'type': 'reservation',
            'period': f"{year}년 {month}월",
            'summary': monthly_stats,
            'chart_data': reservation_chart,
            'generated_at': datetime.now().isoformat()
        }


# 싱글톤 인스턴스
dashboard_service = DashboardService() 