from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from .models import Reservation, PTRecord, ReservationChangeLog
from apps.members.models import Member, MemberPTRegistration
from apps.trainers.models import Trainer, TrainerSchedule, TrainerBlockedTime
from apps.notifications.services import notification_service


class ReservationService:
    """PT 예약 관리 서비스"""
    
    def __init__(self):
        pass
    
    def create_reservation(
        self,
        member: Member,
        trainer: Trainer,
        date: date,
        start_time: str,
        duration: int = 30,
        pt_registration: Optional[MemberPTRegistration] = None,
        repeat_type: str = 'none',
        repeat_end_date: Optional[date] = None,
        notes: str = ''
    ) -> Reservation:
        """PT 예약 생성"""
        
        # 시간 형식 변환
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, '%H:%M').time()
        
        # 종료 시간 계산
        start_datetime = datetime.combine(date, start_time)
        end_datetime = start_datetime + timedelta(minutes=duration)
        end_time = end_datetime.time()
        
        # 예약 가능 여부 확인
        if not self._is_time_available(trainer, date, start_time, end_time):
            raise ValueError("해당 시간대는 예약할 수 없습니다.")
        
        # 회원의 PT 등록 확인
        if pt_registration and pt_registration.remaining_sessions <= 0:
            raise ValueError("남은 PT 횟수가 없습니다.")
        
        with transaction.atomic():
            # 예약 생성
            reservation = Reservation.objects.create(
                member=member,
                trainer=trainer,
                pt_registration=pt_registration,
                date=date,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                repeat_type=repeat_type,
                repeat_end_date=repeat_end_date,
                notes=notes
            )
            
            # 반복 예약 생성
            if repeat_type != 'none' and repeat_end_date:
                self._create_repeat_reservations(reservation)
            
            # 변경 로그 기록
            ReservationChangeLog.objects.create(
                reservation=reservation,
                change_type='created',
                changed_by=f"{member.name} (회원)",
                new_status='pending'
            )
            
            # 트레이너에게 알림 전송
            notification_service.send_reservation_notification(
                reservation=reservation,
                notification_type='reservation_request',
                recipient_type='trainer',
                recipient_id=trainer.id
            )
            
            return reservation
    
    def confirm_reservation(self, reservation: Reservation, confirmed_by: str) -> Reservation:
        """예약 확정"""
        if reservation.reservation_status != 'pending':
            raise ValueError("대기중인 예약만 확정할 수 있습니다.")
        
        with transaction.atomic():
            reservation.reservation_status = 'confirmed'
            reservation.save()
            
            # 변경 로그 기록
            ReservationChangeLog.objects.create(
                reservation=reservation,
                change_type='confirmed',
                changed_by=confirmed_by,
                previous_status='pending',
                new_status='confirmed'
            )
            
            # 회원에게 알림 전송
            notification_service.send_reservation_notification(
                reservation=reservation,
                notification_type='reservation_confirmed',
                recipient_type='member',
                recipient_id=reservation.member.id
            )
            
            return reservation
    
    def reject_reservation(self, reservation: Reservation, rejected_by: str, reason: str = '') -> Reservation:
        """예약 거절"""
        if reservation.reservation_status != 'pending':
            raise ValueError("대기중인 예약만 거절할 수 있습니다.")
        
        with transaction.atomic():
            reservation.reservation_status = 'rejected'
            reservation.notes = f"거절 사유: {reason}\n\n{reservation.notes}"
            reservation.save()
            
            # 변경 로그 기록
            ReservationChangeLog.objects.create(
                reservation=reservation,
                change_type='rejected',
                changed_by=rejected_by,
                previous_status='pending',
                new_status='rejected',
                reason=reason
            )
            
            # 회원에게 알림 전송
            notification_service.send_reservation_notification(
                reservation=reservation,
                notification_type='reservation_rejected',
                recipient_type='member',
                recipient_id=reservation.member.id
            )
            
            return reservation
    
    def cancel_reservation(self, reservation: Reservation, cancelled_by: str, reason: str = '') -> Reservation:
        """예약 취소"""
        if reservation.reservation_status not in ['pending', 'confirmed']:
            raise ValueError("대기중이거나 확정된 예약만 취소할 수 있습니다.")
        
        with transaction.atomic():
            previous_status = reservation.reservation_status
            reservation.reservation_status = 'cancelled'
            reservation.notes = f"취소 사유: {reason}\n\n{reservation.notes}"
            reservation.save()
            
            # 변경 로그 기록
            ReservationChangeLog.objects.create(
                reservation=reservation,
                change_type='cancelled',
                changed_by=cancelled_by,
                previous_status=previous_status,
                new_status='cancelled',
                reason=reason
            )
            
            # 상대방에게 알림 전송
            if previous_status == 'confirmed':
                # 확정된 예약이 취소된 경우
                if cancelled_by == reservation.trainer.name:
                    # 트레이너가 취소한 경우 회원에게 알림
                    notification_service.send_reservation_notification(
                        reservation=reservation,
                        notification_type='reservation_cancelled',
                        recipient_type='member',
                        recipient_id=reservation.member.id
                    )
                else:
                    # 회원이 취소한 경우 트레이너에게 알림
                    notification_service.send_reservation_notification(
                        reservation=reservation,
                        notification_type='reservation_cancelled',
                        recipient_type='trainer',
                        recipient_id=reservation.trainer.id
                    )
            
            return reservation
    
    def complete_pt_session(self, reservation: Reservation, trainer: Trainer, **kwargs) -> PTRecord:
        """PT 세션 완료"""
        if reservation.reservation_status != 'confirmed':
            raise ValueError("확정된 예약만 완료할 수 있습니다.")
        
        with transaction.atomic():
            # 예약 상태 변경
            reservation.reservation_status = 'completed'
            reservation.save()
            
            # PT 수행 내역 생성
            pt_record = PTRecord.objects.create(
                reservation=reservation,
                trainer=trainer,
                member=reservation.member,
                workout_date=reservation.date,
                workout_time=reservation.start_time,
                duration=kwargs.get('duration', reservation.duration),
                content=kwargs.get('content', ''),
                member_condition=kwargs.get('member_condition', ''),
                trainer_notes=kwargs.get('trainer_notes', ''),
                is_completed=True
            )
            
            # 변경 로그 기록
            ReservationChangeLog.objects.create(
                reservation=reservation,
                change_type='completed',
                changed_by=trainer.name,
                previous_status='confirmed',
                new_status='completed'
            )
            
            # PT 등록의 남은 횟수 감소
            if reservation.pt_registration:
                pt_registration = reservation.pt_registration
                pt_registration.remaining_sessions = max(0, pt_registration.remaining_sessions - 1)
                pt_registration.save()
            
            # 완료 알림 전송
            notification_service.send_pt_completion_notification(pt_record)
            
            return pt_record
    
    def _is_time_available(self, trainer: Trainer, date: date, start_time, end_time) -> bool:
        """시간대 예약 가능 여부 확인"""
        # 해당 날짜의 요일
        day_of_week = date.weekday()
        
        # 트레이너 일정 확인
        try:
            schedule = TrainerSchedule.objects.get(
                trainer=trainer,
                day_of_week=day_of_week,
                is_available=True
            )
            
            # 일정 시간대와 겹치는지 확인
            if start_time < schedule.start_time or end_time > schedule.end_time:
                return False
        except TrainerSchedule.DoesNotExist:
            return False
        
        # 차단된 시간 확인
        blocked_times = TrainerBlockedTime.objects.filter(
            trainer=trainer,
            date=date
        )
        
        for blocked_time in blocked_times:
            if (start_time < blocked_time.end_time and end_time > blocked_time.start_time):
                return False
        
        # 기존 예약과 겹치는지 확인
        existing_reservations = Reservation.objects.filter(
            trainer=trainer,
            date=date,
            reservation_status__in=['pending', 'confirmed']
        )
        
        for existing in existing_reservations:
            if (start_time < existing.end_time and end_time > existing.start_time):
                return False
        
        return True
    
    def _create_repeat_reservations(self, original_reservation: Reservation):
        """반복 예약 생성"""
        if original_reservation.repeat_type == 'none':
            return
        
        current_date = original_reservation.date + timedelta(days=1)
        end_date = original_reservation.repeat_end_date
        
        while current_date <= end_date:
            if original_reservation.repeat_type == 'daily':
                # 매일
                if self._is_time_available(
                    original_reservation.trainer,
                    current_date,
                    original_reservation.start_time,
                    original_reservation.end_time
                ):
                    Reservation.objects.create(
                        member=original_reservation.member,
                        trainer=original_reservation.trainer,
                        pt_registration=original_reservation.pt_registration,
                        date=current_date,
                        start_time=original_reservation.start_time,
                        end_time=original_reservation.end_time,
                        duration=original_reservation.duration,
                        repeat_type='none',  # 반복 예약은 개별 예약으로 생성
                        notes=original_reservation.notes
                    )
                current_date += timedelta(days=1)
                
            elif original_reservation.repeat_type == 'weekly':
                # 매주 같은 요일
                if current_date.weekday() == original_reservation.date.weekday():
                    if self._is_time_available(
                        original_reservation.trainer,
                        current_date,
                        original_reservation.start_time,
                        original_reservation.end_time
                    ):
                        Reservation.objects.create(
                            member=original_reservation.member,
                            trainer=original_reservation.trainer,
                            pt_registration=original_reservation.pt_registration,
                            date=current_date,
                            start_time=original_reservation.start_time,
                            end_time=original_reservation.end_time,
                            duration=original_reservation.duration,
                            repeat_type='none',
                            notes=original_reservation.notes
                        )
                current_date += timedelta(days=1)
    
    def get_trainer_available_times(self, trainer: Trainer, date: date) -> List[Dict[str, Any]]:
        """트레이너의 예약 가능 시간대 조회"""
        available_times = []
        
        # 해당 날짜의 요일
        day_of_week = date.weekday()
        
        try:
            schedule = TrainerSchedule.objects.get(
                trainer=trainer,
                day_of_week=day_of_week,
                is_available=True
            )
            
            # 30분 단위로 시간대 생성
            current_time = schedule.start_time
            while current_time < schedule.end_time:
                end_time = (datetime.combine(date, current_time) + timedelta(minutes=30)).time()
                
                if self._is_time_available(trainer, date, current_time, end_time):
                    available_times.append({
                        'start_time': current_time.strftime('%H:%M'),
                        'end_time': end_time.strftime('%H:%M'),
                        'available': True
                    })
                else:
                    available_times.append({
                        'start_time': current_time.strftime('%H:%M'),
                        'end_time': end_time.strftime('%H:%M'),
                        'available': False
                    })
                
                current_time = end_time
                
        except TrainerSchedule.DoesNotExist:
            pass
        
        return available_times
    
    def get_member_reservations(
        self, 
        member: Member, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status: Optional[str] = None
    ) -> List[Reservation]:
        """회원의 예약 목록 조회"""
        queryset = Reservation.objects.filter(member=member)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if status:
            queryset = queryset.filter(reservation_status=status)
        
        return queryset.order_by('date', 'start_time')
    
    def get_trainer_reservations(
        self, 
        trainer: Trainer, 
        date: Optional[date] = None,
        status: Optional[str] = None
    ) -> List[Reservation]:
        """트레이너의 예약 목록 조회"""
        queryset = Reservation.objects.filter(trainer=trainer)
        
        if date:
            queryset = queryset.filter(date=date)
        if status:
            queryset = queryset.filter(reservation_status=status)
        
        return queryset.order_by('date', 'start_time')
    
    def get_branch_reservations(
        self, 
        branch_id: int, 
        date: Optional[date] = None,
        status: Optional[str] = None
    ) -> List[Reservation]:
        """지점의 예약 목록 조회"""
        queryset = Reservation.objects.filter(
            Q(member__branch_id=branch_id) | Q(trainer__branch_id=branch_id)
        )
        
        if date:
            queryset = queryset.filter(date=date)
        if status:
            queryset = queryset.filter(reservation_status=status)
        
        return queryset.order_by('date', 'start_time')


# 싱글톤 인스턴스
reservation_service = ReservationService() 