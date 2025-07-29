# Clamood Gym - 헬스장 회원관리 시스템

Django 기반의 종합적인 헬스장 회원관리 시스템입니다. 다중 지점 운영, PT 예약 관리, 트레이너 급여 계산, 알림 시스템 등을 포함한 완전한 솔루션을 제공합니다.

## 🏗️ 시스템 아키텍처

### 기술 스택

- **Backend**: Django 4.2, Python 3.11
- **Frontend**: React 18, TypeScript, Styled Components
- **Database**: SQLite (개발) / PostgreSQL (운영)
- **Task Queue**: Celery + Redis
- **API**: Django REST Framework
- **Authentication**: Django Token Authentication

### 프로젝트 구조

```
clamood_gym/
├── apps/                    # Django 앱들
│   ├── branches/           # 지점 관리
│   ├── members/            # 회원 관리
│   ├── trainers/           # 트레이너 관리
│   ├── reservations/       # 예약 관리
│   ├── salaries/           # 급여 관리
│   ├── notifications/      # 알림 시스템
│   └── dashboards/         # 대시보드
├── frontend/               # React 프론트엔드
├── scripts/                # 유틸리티 스크립트
└── clamood_gym/           # 프로젝트 설정
```

## 🚀 주요 기능

### 1. 지점 관리

- **다중 지점 운영**: 본사와 지점별 독립적인 데이터 관리
- **권한 관리**: 본사 어드민(전체 관리) vs 지점 어드민(자기 지점만)
- **지점별 통계**: 매출, 회원, 트레이너 현황

### 2. 회원 관리

- **회원 정보 관리**: 기본 정보, 연락처, 회원 상태
- **PT 프로그램**: 신규/장기/단기 프로그램별 가격 설정
- **PT 등록 관리**: 프로그램별 횟수, 만료일, 진행 상황
- **회원 상태 추적**: 활성/비활성/정지/만료

### 3. 트레이너 관리

- **트레이너 정보**: 기본 정보, 전문 분야, 자격증
- **일정 관리**: 요일별 근무 시간 설정
- **차단 시간**: 특정 시간대 예약 차단
- **인센티브 설정**: 고정 금액 또는 퍼센티지 방식

### 4. PT 예약 시스템

- **30분 단위 예약**: 정확한 시간대 예약
- **반복 예약**: 매일/매주/매월 반복 예약
- **예약 상태 관리**: 대기/확정/거절/취소/완료
- **시간대 충돌 방지**: 자동 중복 체크

### 5. 급여 관리

- **자동 급여 계산**: 기본급 + 인센티브 + 추가매출 - 기타비용
- **월별 급여**: 매월 자동 계산 및 지급
- **상세 내역**: 인센티브, 추가매출, 기타비용 상세
- **지점별 매출**: PT, 회원권, 추가 매출 통계

### 6. 알림 시스템

- **카카오톡 연동**: 실제 카카오톡 API를 통한 푸시 알림
- **다양한 알림 유형**: 예약 요청/확정/거절, PT 완료, 급여 지급
- **알림 로그**: 전송 성공/실패 로그 관리
- **자동 알림**: 예약 알림, 만료 예정 알림, 생일 축하

### 7. 대시보드 & 통계

- **실시간 통계**: 회원, 트레이너, 예약, 매출 현황
- **차트 시각화**: 매출 추이, 예약 현황, 회원 증가
- **지점별 비교**: 지점간 성과 비교
- **트레이너 성과**: 개인별 PT 완료율, 급여

### 8. 자동화 기능

- **Celery 태스크**: 백그라운드 작업 처리
- **스케줄링**: 매일/매주/매월 자동 실행
- **데이터 정리**: 오래된 알림 자동 삭제
- **실패 재시도**: 알림 전송 실패 시 자동 재시도

## 📋 요구사항

### 시스템 요구사항

- Python 3.11+
- Node.js 16+
- Redis (Celery용)
- PostgreSQL (운영 환경)

### Python 패키지

```
Django==4.2.7
djangorestframework==3.14.0
celery==5.3.4
redis==5.0.1
requests==2.31.0
django-cors-headers==4.3.1
django-filter==23.3
Pillow==10.1.0
django-model-utils==4.3.1
```

### Node.js 패키지

```
react==18.2.0
typescript==5.2.2
styled-components==6.1.1
axios==1.6.2
react-router-dom==6.20.1
```

## 🛠️ 설치 및 실행

### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd clamood_gym
```

### 2. Python 환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 3. 데이터베이스 설정

```bash
# 마이그레이션 실행
python manage.py makemigrations
python manage.py migrate

# 샘플 데이터 생성
python scripts/create_sample_data.py
```

### 4. 환경 변수 설정

```bash
# .env 파일 생성
cp env_example.txt .env

# 필요한 환경 변수 설정
SECRET_KEY=your-secret-key
DEBUG=True
KAKAO_API_KEY=your-kakao-api-key
CELERY_BROKER_URL=redis://localhost:6379/0
```

### 5. Redis 설치 및 실행

```bash
# Windows (WSL 또는 Docker 사용 권장)
# macOS
brew install redis
brew services start redis

# Ubuntu
sudo apt-get install redis-server
sudo systemctl start redis
```

### 6. Celery 실행

```bash
# Celery Worker 실행
celery -A clamood_gym worker -l info

# Celery Beat 실행 (새 터미널)
celery -A clamood_gym beat -l info
```

### 7. Django 서버 실행

```bash
python manage.py runserver
```

### 8. 프론트엔드 실행

```bash
cd frontend
npm install
npm start
```

## 🔐 기본 로그인 정보

샘플 데이터 생성 후 사용 가능한 계정:

### 본사 어드민

- **Username**: `headquarters_admin`
- **Password**: `password123`
- **권한**: 전체 지점 관리

### 지점 어드민

- **Username**: `branch_admin_1`
- **Password**: `password123`
- **권한**: 해당 지점만 관리

## 📱 API 문서

### 주요 API 엔드포인트

#### 인증

- `POST /api/auth/login/` - 로그인
- `POST /api/auth/logout/` - 로그아웃

#### 지점 관리

- `GET /api/branches/` - 지점 목록
- `GET /api/branches/{id}/` - 지점 상세

#### 회원 관리

- `GET /api/members/` - 회원 목록
- `POST /api/members/` - 회원 등록
- `GET /api/members/{id}/` - 회원 상세
- `PUT /api/members/{id}/` - 회원 수정

#### 트레이너 관리

- `GET /api/trainers/` - 트레이너 목록
- `POST /api/trainers/` - 트레이너 등록
- `GET /api/trainers/{id}/schedule/` - 트레이너 일정

#### 예약 관리

- `GET /api/reservations/` - 예약 목록
- `POST /api/reservations/` - 예약 생성
- `PUT /api/reservations/{id}/confirm/` - 예약 확정
- `PUT /api/reservations/{id}/reject/` - 예약 거절

#### 급여 관리

- `GET /api/salaries/` - 급여 목록
- `POST /api/salaries/calculate/` - 급여 계산
- `GET /api/salaries/{id}/` - 급여 상세

#### 알림 관리

- `GET /api/notifications/` - 알림 목록
- `PUT /api/notifications/{id}/read/` - 읽음 처리
- `DELETE /api/notifications/{id}/` - 알림 삭제

## 🔧 개발 가이드

### 새로운 기능 추가

#### 1. 모델 생성

```python
# apps/your_app/models.py
from django.db import models

class YourModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Your Model'
        verbose_name_plural = 'Your Models'
```

#### 2. 시리얼라이저 생성

```python
# apps/your_app/serializers.py
from rest_framework import serializers
from .models import YourModel

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = '__all__'
```

#### 3. 뷰 생성

```python
# apps/your_app/views.py
from rest_framework import viewsets
from .models import YourModel
from .serializers import YourModelSerializer

class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
```

#### 4. URL 설정

```python
# apps/your_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import YourModelViewSet

router = DefaultRouter()
router.register(r'your-models', YourModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### Celery 태스크 추가

```python
# apps/your_app/tasks.py
from celery import shared_task

@shared_task
def your_task():
    """새로운 백그라운드 태스크"""
    print("태스크 실행 중...")
    return "완료"
```

### 프론트엔드 컴포넌트 추가

```typescript
// frontend/src/components/YourComponent.tsx
import React from "react";
import styled from "styled-components";

const Container = styled.div`
  padding: 20px;
`;

const YourComponent: React.FC = () => {
  return (
    <Container>
      <h1>새로운 컴포넌트</h1>
    </Container>
  );
};

export default YourComponent;
```

## 🧪 테스트

### 백엔드 테스트

```bash
# 전체 테스트 실행
python manage.py test

# 특정 앱 테스트
python manage.py test apps.members
```

### 프론트엔드 테스트

```bash
cd frontend
npm test
```

## 📊 모니터링

### 로그 확인

```bash
# Django 로그
tail -f logs/django.log

# Celery 로그
tail -f logs/celery.log
```

### 성능 모니터링

- Django Debug Toolbar (개발 환경)
- Celery Flower (태스크 모니터링)

## 🚀 배포

### Docker 배포

```bash
# Docker 이미지 빌드
docker build -t clamood-gym .

# 컨테이너 실행
docker-compose up -d
```

### 수동 배포

```bash
# 정적 파일 수집
python manage.py collectstatic

# 데이터베이스 마이그레이션
python manage.py migrate

# Gunicorn 실행
gunicorn clamood_gym.wsgi:application
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

- **이메일**: support@clamood.com
- **문서**: [API Documentation](API_DOCUMENTATION.md)
- **이슈**: [GitHub Issues](https://github.com/your-repo/issues)

## 🔄 업데이트 로그

### v1.0.0 (2024-01-15)

- 초기 릴리즈
- 기본 CRUD 기능
- 예약 시스템
- 급여 계산
- 알림 시스템
- 대시보드

---

**Clamood Gym** - 헬스장 회원관리 시스템의 완벽한 솔루션
