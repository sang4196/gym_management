import requests
import logging
from typing import Dict, Any, Optional
from django.conf import settings
from django.utils import timezone
from .models import Notification, NotificationLog

logger = logging.getLogger(__name__)


class KakaoNotificationService:
    """카카오톡 알림 전송 서비스"""
    
    def __init__(self):
        self.api_key = settings.KAKAO_API_KEY
        self.base_url = "https://kapi.kakao.com"
        
    def send_notification(self, notification: Notification) -> bool:
        """알림 전송"""
        try:
            # 수신자 정보 가져오기
            recipient = notification.get_recipient()
            if not recipient:
                self._log_failure(notification, "수신자를 찾을 수 없습니다.")
                return False
            
            # 카카오톡 ID 확인
            if hasattr(recipient, 'kakao_id') and recipient.kakao_id:
                kakao_id = recipient.kakao_id
            else:
                self._log_failure(notification, "카카오톡 ID가 없습니다.")
                return False
            
            # 메시지 템플릿 생성
            template_data = self._create_template_data(notification)
            
            # 카카오톡 API 호출
            success = self._send_kakao_message(kakao_id, template_data)
            
            if success:
                # 성공 로그 기록
                self._log_success(notification, kakao_id, template_data)
                # 알림 상태 업데이트
                notification.kakao_sent = True
                notification.kakao_sent_at = timezone.now()
                notification.save()
                return True
            else:
                self._log_failure(notification, "카카오톡 API 호출 실패")
                return False
                
        except Exception as e:
            logger.error(f"카카오톡 알림 전송 실패: {str(e)}")
            self._log_failure(notification, str(e))
            return False
    
    def _create_template_data(self, notification: Notification) -> Dict[str, Any]:
        """템플릿 데이터 생성"""
        template_data = {
            "object_type": "text",
            "text": notification.message,
            "link": {
                "web_url": f"{settings.SITE_URL}/notifications/{notification.id}",
                "mobile_web_url": f"{settings.SITE_URL}/notifications/{notification.id}"
            }
        }
        
        # 알림 유형에 따른 추가 데이터
        if notification.notification_type == 'reservation_request':
            template_data["text"] = f"🔔 {notification.title}\n\n{notification.message}"
        elif notification.notification_type == 'reservation_confirmed':
            template_data["text"] = f"✅ {notification.title}\n\n{notification.message}"
        elif notification.notification_type == 'reservation_rejected':
            template_data["text"] = f"❌ {notification.title}\n\n{notification.message}"
        elif notification.notification_type == 'pt_completed':
            template_data["text"] = f"🎯 {notification.title}\n\n{notification.message}"
        elif notification.notification_type == 'salary_paid':
            template_data["text"] = f"💰 {notification.title}\n\n{notification.message}"
        
        return template_data
    
    def _send_kakao_message(self, kakao_id: str, template_data: Dict[str, Any]) -> bool:
        """카카오톡 메시지 전송"""
        try:
            url = f"{self.base_url}/v1/api/talk/friends/message/default/send"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {
                "receiver_uuids": f'["{kakao_id}"]',
                "template_object": str(template_data)
            }
            
            response = requests.post(url, headers=headers, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("successful_receiver_uuids"):
                    return True
                else:
                    logger.error(f"카카오톡 전송 실패: {result}")
                    return False
            else:
                logger.error(f"카카오톡 API 오류: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"카카오톡 API 요청 실패: {str(e)}")
            return False
    
    def _log_success(self, notification: Notification, recipient: str, message: str):
        """성공 로그 기록"""
        NotificationLog.objects.create(
            notification=notification,
            log_type='kakao_success',
            recipient=recipient,
            message=str(message),
            response="전송 성공"
        )
    
    def _log_failure(self, notification: Notification, error_message: str):
        """실패 로그 기록"""
        NotificationLog.objects.create(
            notification=notification,
            log_type='kakao_failed',
            recipient="",
            message="",
            error_message=error_message
        )


class NotificationService:
    """알림 서비스 통합 관리"""
    
    def __init__(self):
        self.kakao_service = KakaoNotificationService()
    
    def send_notification(self, notification: Notification) -> bool:
        """알림 전송 (모든 채널)"""
        success = False
        
        # 카카오톡 전송
        if self._should_send_kakao(notification):
            success = self.kakao_service.send_notification(notification)
        
        # 알림 상태 업데이트
        if success:
            notification.status = 'sent'
        else:
            notification.status = 'failed'
        
        notification.save()
        return success
    
    def _should_send_kakao(self, notification: Notification) -> bool:
        """카카오톡 전송 여부 확인"""
        # 알림 설정 확인
        recipient = notification.get_recipient()
        if not recipient:
            return False
        
        # 기본적으로 카카오톡 전송 활성화
        return True
    
    def create_notification(
        self,
        notification_type: str,
        recipient_type: str,
        recipient_id: int,
        title: str,
        message: str,
        priority: str = 'medium',
        related_reservation: Optional[int] = None
    ) -> Notification:
        """알림 생성 및 전송"""
        notification = Notification.objects.create(
            notification_type=notification_type,
            recipient_type=recipient_type,
            recipient_id=recipient_id,
            title=title,
            message=message,
            priority=priority,
            related_reservation_id=related_reservation
        )
        
        # 즉시 전송
        self.send_notification(notification)
        
        return notification
    
    def send_reservation_notification(
        self,
        reservation,
        notification_type: str,
        recipient_type: str,
        recipient_id: int
    ):
        """예약 관련 알림 전송"""
        if notification_type == 'reservation_request':
            title = "새로운 PT 예약 요청"
            message = f"{reservation.member.name} 회원님이 {reservation.date} {reservation.start_time}에 PT 예약을 요청했습니다."
        elif notification_type == 'reservation_confirmed':
            title = "PT 예약이 확정되었습니다"
            message = f"{reservation.date} {reservation.start_time} PT 예약이 확정되었습니다."
        elif notification_type == 'reservation_rejected':
            title = "PT 예약이 거절되었습니다"
            message = f"{reservation.date} {reservation.start_time} PT 예약이 거절되었습니다."
        elif notification_type == 'reservation_cancelled':
            title = "PT 예약이 취소되었습니다"
            message = f"{reservation.date} {reservation.start_time} PT 예약이 취소되었습니다."
        elif notification_type == 'reservation_reminder':
            title = "PT 예약 알림"
            message = f"내일 {reservation.start_time}에 PT 예약이 있습니다. 준비해주세요."
        else:
            return None
        
        return self.create_notification(
            notification_type=notification_type,
            recipient_type=recipient_type,
            recipient_id=recipient_id,
            title=title,
            message=message,
            related_reservation=reservation.id
        )
    
    def send_pt_completion_notification(self, pt_record):
        """PT 완료 알림 전송"""
        title = "PT 세션이 완료되었습니다"
        message = f"{pt_record.member.name} 회원님의 PT 세션이 성공적으로 완료되었습니다. 수행 내역을 확인해주세요."
        
        return self.create_notification(
            notification_type='pt_completed',
            recipient_type='trainer',
            recipient_id=pt_record.trainer.id,
            title=title,
            message=message,
            related_reservation=pt_record.reservation.id
        )
    
    def send_salary_notification(self, salary):
        """급여 지급 알림 전송"""
        title = "급여 지급 완료"
        message = f"{salary.year}년 {salary.month}월 급여가 지급되었습니다. 총 {salary.total_salary:,}원"
        
        return self.create_notification(
            notification_type='salary_paid',
            recipient_type='trainer',
            recipient_id=salary.trainer.id,
            title=title,
            message=message
        )


# 싱글톤 인스턴스
notification_service = NotificationService() 