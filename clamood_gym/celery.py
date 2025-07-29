import os
from celery import Celery
from django.conf import settings

# Django 설정 모듈 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clamood_gym.settings')

# Celery 앱 생성
app = Celery('clamood_gym')

# Django 설정에서 Celery 설정 로드
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django 앱에서 태스크 자동 발견
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Celery Beat 스케줄 설정
app.conf.beat_schedule = {
    # 매일 오전 9시에 예약 알림 전송
    'send-reservation-reminders': {
        'task': 'apps.notifications.tasks.send_reservation_reminders',
        'schedule': 86400.0,  # 24시간 (초 단위)
    },
    
    # 매일 오전 8시에 일일 알림 전송
    'send-daily-notifications': {
        'task': 'apps.notifications.tasks.send_daily_notifications',
        'schedule': 86400.0,  # 24시간
    },
    
    # 매월 1일 오전 6시에 급여 계산
    'calculate-monthly-salaries': {
        'task': 'apps.notifications.tasks.calculate_monthly_salaries',
        'schedule': 2592000.0,  # 30일 (초 단위)
    },
    
    # 매월 1일 오전 7시에 매출 계산
    'calculate-monthly-revenues': {
        'task': 'apps.notifications.tasks.calculate_monthly_revenues',
        'schedule': 2592000.0,  # 30일
    },
    
    # 매주 월요일 오전 9시에 주간 리포트 전송
    'send-weekly-reports': {
        'task': 'apps.notifications.tasks.send_weekly_reports',
        'schedule': 604800.0,  # 7일
    },
    
    # 매월 1일 오전 10시에 월간 리포트 전송
    'send-monthly-reports': {
        'task': 'apps.notifications.tasks.send_monthly_reports',
        'schedule': 2592000.0,  # 30일
    },
    
    # 매일 오전 8시에 만료 예정 PT 등록 확인
    'check-expiring-pt-registrations': {
        'task': 'apps.notifications.tasks.check_expiring_pt_registrations',
        'schedule': 86400.0,  # 24시간
    },
    
    # 매일 오전 9시에 만료된 PT 등록 상태 업데이트
    'update-expired-pt-registrations': {
        'task': 'apps.notifications.tasks.update_expired_pt_registrations',
        'schedule': 86400.0,  # 24시간
    },
    
    # 매일 오전 10시에 생일 알림 전송
    'send-birthday-notifications': {
        'task': 'apps.notifications.tasks.send_birthday_notifications',
        'schedule': 86400.0,  # 24시간
    },
    
    # 매주 일요일 오전 2시에 오래된 알림 정리
    'cleanup-old-notifications': {
        'task': 'apps.notifications.tasks.cleanup_old_notifications',
        'schedule': 604800.0,  # 7일
    },
    
    # 매시간 실패한 알림 재전송
    'retry-failed-notifications': {
        'task': 'apps.notifications.tasks.retry_failed_notifications',
        'schedule': 3600.0,  # 1시간
    },
}

# 태스크 결과 설정
app.conf.result_expires = 3600  # 1시간 후 결과 만료

# 태스크 타임아웃 설정
app.conf.task_soft_time_limit = 300  # 5분
app.conf.task_time_limit = 600  # 10분

# 워커 설정
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_max_tasks_per_child = 1000

# 로깅 설정
app.conf.worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
app.conf.worker_task_log_format = '[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s'

@app.task(bind=True)
def debug_task(self):
    """디버그용 태스크"""
    print(f'Request: {self.request!r}')

@app.task(bind=True)
def test_task(self):
    """테스트용 태스크"""
    print('테스트 태스크 실행 중...')
    return '테스트 태스크 완료'

if __name__ == '__main__':
    app.start() 