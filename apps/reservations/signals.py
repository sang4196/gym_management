from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.reservations.models import Reservation, PTRecord, ReservationChangeLog
from apps.notifications.tasks import (
    send_reservation_request_notification,
    send_reservation_status_notification,
    send_pt_completion_notification
)


@receiver(post_save, sender=Reservation)
def handle_reservation_save(sender, instance, created, **kwargs):
    """예약 저장 시 처리"""
    if created:
        # 새 예약 생성 시 트레이너에게 알림 (개발 환경에서는 동기 실행)
        try:
            send_reservation_request_notification.delay(instance.id)
        except:
            # Redis 연결 실패 시 무시
            pass
        
        # 변경 로그 기록
        ReservationChangeLog.objects.create(
            reservation=instance,
            change_type='created',
            changed_by='system',
            new_status=instance.reservation_status
        )
    else:
        # 예약 상태 변경 시 알림
        if instance.tracker.has_changed('reservation_status'):
            old_status = instance.tracker.previous('reservation_status')
            new_status = instance.reservation_status
            
            # 상태가 변경된 경우에만 알림 전송
            if old_status != new_status:
                try:
                    send_reservation_status_notification.delay(instance.id, new_status)
                except:
                    # Redis 연결 실패 시 무시
                    pass
                
                # 변경 로그 기록
                ReservationChangeLog.objects.create(
                    reservation=instance,
                    change_type='modified',
                    changed_by='system',
                    previous_status=old_status,
                    new_status=new_status
                )


@receiver(post_save, sender=PTRecord)
def handle_pt_record_save(sender, instance, created, **kwargs):
    """PT 기록 저장 시 처리"""
    if created and instance.is_completed:
        # PT 완료 시 알림
        try:
            send_pt_completion_notification.delay(instance.id)
        except:
            # Redis 연결 실패 시 무시
            pass
    
    elif not created and instance.tracker.has_changed('is_completed'):
        # PT 완료 상태가 변경된 경우
        if instance.is_completed:
            try:
                send_pt_completion_notification.delay(instance.id)
            except:
                # Redis 연결 실패 시 무시
                pass


@receiver(post_delete, sender=Reservation)
def handle_reservation_delete(sender, instance, **kwargs):
    """예약 삭제 시 처리"""
    # 변경 로그 기록
    ReservationChangeLog.objects.create(
        reservation=instance,
        change_type='cancelled',
        changed_by='system',
        previous_status=instance.reservation_status,
        reason='예약 삭제'
    ) 