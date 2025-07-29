# Clamood Gym API Documentation

헬스장 회원관리 시스템의 REST API 문서입니다.

## 📋 개요

- **Base URL**: `http://localhost:8000/api/`
- **Content-Type**: `application/json`
- **Authentication**: Token Authentication
- **Version**: v1.0.0

## 🔐 인증

### 로그인

```http
POST /api/auth/login/
```

**Request Body:**

```json
{
  "username": "headquarters_admin",
  "password": "password123"
}
```

**Response:**

```json
{
  "token": "your-auth-token",
  "user": {
    "id": 1,
    "username": "headquarters_admin",
    "email": "headquarters@clamood.com",
    "admin_type": "headquarters",
    "branch": null
  }
}
```

### 로그아웃

```http
POST /api/auth/logout/
```

**Headers:**

```
Authorization: Token your-auth-token
```

## 🏢 지점 관리

### 지점 목록 조회

```http
GET /api/branches/
```

**Query Parameters:**

- `is_active` (boolean): 활성화된 지점만 조회
- `search` (string): 지점명 검색

**Response:**

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "강남점",
      "address": "서울특별시 강남구 테헤란로 123",
      "phone": "02-1234-5678",
      "email": "gangnam@clamood.com",
      "is_active": true,
      "created_at": "2024-01-15T00:00:00Z"
    }
  ]
}
```

### 지점 상세 조회

```http
GET /api/branches/{id}/
```

**Response:**

```json
{
  "id": 1,
  "name": "강남점",
  "address": "서울특별시 강남구 테헤란로 123",
  "phone": "02-1234-5678",
  "email": "gangnam@clamood.com",
  "is_active": true,
  "created_at": "2024-01-15T00:00:00Z",
  "updated_at": "2024-01-15T00:00:00Z",
  "stats": {
    "total_members": 24,
    "total_trainers": 3,
    "monthly_revenue": 15000000
  }
}
```

## 👥 회원 관리

### 회원 목록 조회

```http
GET /api/members/
```

**Query Parameters:**

- `branch` (integer): 지점 ID 필터
- `membership_status` (string): 회원 상태 필터
- `search` (string): 이름/전화번호 검색
- `registration_date_after` (date): 가입일 이후
- `registration_date_before` (date): 가입일 이전

**Response:**

```json
{
  "count": 24,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "김회원1",
      "phone": "010-4000-4000",
      "email": "member1@example.com",
      "gender": "M",
      "birth_date": "1990-05-15",
      "membership_status": "active",
      "registration_date": "2024-01-01",
      "branch": {
        "id": 1,
        "name": "강남점"
      }
    }
  ]
}
```

### 회원 등록

```http
POST /api/members/
```

**Request Body:**

```json
{
  "name": "새회원",
  "phone": "010-9999-9999",
  "email": "newmember@example.com",
  "gender": "F",
  "birth_date": "1995-08-20",
  "address": "서울시 강남구",
  "emergency_contact": "010-8888-8888",
  "branch": 1
}
```

### 회원 상세 조회

```http
GET /api/members/{id}/
```

**Response:**

```json
{
  "id": 1,
  "name": "김회원1",
  "phone": "010-4000-4000",
  "email": "member1@example.com",
  "gender": "M",
  "birth_date": "1990-05-15",
  "address": "강남점 근처 주소",
  "emergency_contact": "010-5000-5000",
  "membership_status": "active",
  "registration_date": "2024-01-01",
  "expiry_date": null,
  "notes": "",
  "branch": {
    "id": 1,
    "name": "강남점"
  },
  "pt_registrations": [
    {
      "id": 1,
      "pt_program": {
        "id": 1,
        "name": "신규 회원 PT",
        "sessions": 10,
        "price": "500000.00"
      },
      "total_sessions": 10,
      "remaining_sessions": 7,
      "registration_status": "active",
      "expiry_date": "2024-07-01"
    }
  ]
}
```

### 회원 수정

```http
PUT /api/members/{id}/
```

**Request Body:**

```json
{
  "name": "김회원1",
  "phone": "010-4000-4000",
  "email": "updated@example.com",
  "membership_status": "active"
}
```

## 💪 트레이너 관리

### 트레이너 목록 조회

```http
GET /api/trainers/
```

**Query Parameters:**

- `branch` (integer): 지점 ID 필터
- `employment_status` (string): 재직 상태 필터
- `search` (string): 이름/전화번호 검색

**Response:**

```json
{
  "count": 9,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "김철수 (강남점)",
      "phone": "010-1111-1111",
      "email": "trainer1@clamood.com",
      "gender": "M",
      "employment_status": "active",
      "base_salary": "2500000.00",
      "experience_years": 3,
      "branch": {
        "id": 1,
        "name": "강남점"
      }
    }
  ]
}
```

### 트레이너 등록

```http
POST /api/trainers/
```

**Request Body:**

```json
{
  "name": "새트레이너",
  "phone": "010-7777-7777",
  "email": "newtrainer@clamood.com",
  "gender": "M",
  "birth_date": "1988-03-15",
  "base_salary": "2800000",
  "hire_date": "2024-01-15",
  "experience_years": 5,
  "specialties": "웨이트 트레이닝, 다이어트",
  "certifications": "생활스포츠지도사 2급",
  "branch": 1
}
```

### 트레이너 일정 조회

```http
GET /api/trainers/{id}/schedule/
```

**Response:**

```json
{
  "trainer": {
    "id": 1,
    "name": "김철수 (강남점)"
  },
  "schedules": [
    {
      "day_of_week": 0,
      "day_name": "월요일",
      "start_time": "09:00:00",
      "end_time": "18:00:00",
      "is_available": true
    }
  ],
  "blocked_times": [
    {
      "date": "2024-01-20",
      "start_time": "14:00:00",
      "end_time": "16:00:00",
      "reason": "개인 일정"
    }
  ]
}
```

### 트레이너 인센티브 설정

```http
POST /api/trainers/{id}/incentive/
```

**Request Body:**

```json
{
  "incentive_type": "fixed",
  "fixed_amount": "50000",
  "percentage_rate": "0",
  "is_active": true
}
```

## 📅 예약 관리

### 예약 목록 조회

```http
GET /api/reservations/
```

**Query Parameters:**

- `member` (integer): 회원 ID 필터
- `trainer` (integer): 트레이너 ID 필터
- `date` (date): 예약 날짜 필터
- `reservation_status` (string): 예약 상태 필터
- `date_after` (date): 날짜 이후
- `date_before` (date): 날짜 이전

**Response:**

```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "member": {
        "id": 1,
        "name": "김회원1"
      },
      "trainer": {
        "id": 1,
        "name": "김철수 (강남점)"
      },
      "date": "2024-01-20",
      "start_time": "14:00:00",
      "end_time": "14:30:00",
      "duration": 30,
      "reservation_status": "confirmed",
      "repeat_type": "none",
      "notes": ""
    }
  ]
}
```

### 예약 생성

```http
POST /api/reservations/
```

**Request Body:**

```json
{
  "member": 1,
  "trainer": 1,
  "date": "2024-01-25",
  "start_time": "15:00",
  "duration": 30,
  "pt_registration": 1,
  "repeat_type": "none",
  "notes": "첫 PT 세션"
}
```

### 예약 확정

```http
PUT /api/reservations/{id}/confirm/
```

**Request Body:**

```json
{
  "confirmed_by": "김철수 트레이너"
}
```

### 예약 거절

```http
PUT /api/reservations/{id}/reject/
```

**Request Body:**

```json
{
  "rejected_by": "김철수 트레이너",
  "reason": "개인 일정으로 인한 거절"
}
```

### 예약 취소

```http
PUT /api/reservations/{id}/cancel/
```

**Request Body:**

```json
{
  "cancelled_by": "김회원1",
  "reason": "개인 사정으로 인한 취소"
}
```

### 트레이너 예약 가능 시간 조회

```http
GET /api/trainers/{id}/available-times/?date=2024-01-25
```

**Response:**

```json
{
  "trainer": {
    "id": 1,
    "name": "김철수 (강남점)"
  },
  "date": "2024-01-25",
  "available_times": [
    {
      "start_time": "09:00",
      "end_time": "09:30",
      "available": true
    },
    {
      "start_time": "09:30",
      "end_time": "10:00",
      "available": false
    }
  ]
}
```

## 💰 급여 관리

### 급여 목록 조회

```http
GET /api/salaries/
```

**Query Parameters:**

- `trainer` (integer): 트레이너 ID 필터
- `year` (integer): 년도 필터
- `month` (integer): 월 필터
- `payment_status` (string): 지급 상태 필터

**Response:**

```json
{
  "count": 27,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "trainer": {
        "id": 1,
        "name": "김철수 (강남점)"
      },
      "year": 2024,
      "month": 1,
      "base_salary": "2500000.00",
      "incentive_amount": "150000.00",
      "additional_revenue": "50000.00",
      "other_costs": "20000.00",
      "total_salary": "2680000.00",
      "payment_status": "paid",
      "payment_date": "2024-01-25"
    }
  ]
}
```

### 급여 계산

```http
POST /api/salaries/calculate/
```

**Request Body:**

```json
{
  "trainer_id": 1,
  "year": 2024,
  "month": 1,
  "force_recalculate": false
}
```

### 급여 상세 조회

```http
GET /api/salaries/{id}/
```

**Response:**

```json
{
  "id": 1,
  "trainer": {
    "id": 1,
    "name": "김철수 (강남점)"
  },
  "year": 2024,
  "month": 1,
  "base_salary": "2500000.00",
  "incentive_amount": "150000.00",
  "additional_revenue": "50000.00",
  "other_costs": "20000.00",
  "total_salary": "2680000.00",
  "payment_status": "paid",
  "payment_date": "2024-01-25",
  "incentive_details": [
    {
      "incentive_type": "pt_session",
      "quantity": 3,
      "unit_amount": "50000.00",
      "total_amount": "150000.00",
      "description": "2024년 1월 PT 세션 3회"
    }
  ],
  "additional_revenues": [],
  "other_cost_items": []
}
```

## 🔔 알림 관리

### 알림 목록 조회

```http
GET /api/notifications/
```

**Query Parameters:**

- `notification_type` (string): 알림 유형 필터
- `status` (string): 상태 필터
- `priority` (string): 우선순위 필터
- `read_at` (boolean): 읽음 여부 필터

**Response:**

```json
{
  "count": 20,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "notification_type": "reservation_request",
      "title": "새로운 PT 예약 요청",
      "message": "김회원1 회원님이 2024-01-20 14:00에 PT 예약을 요청했습니다.",
      "priority": "medium",
      "status": "sent",
      "kakao_sent": true,
      "read_at": null,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 알림 읽음 처리

```http
PUT /api/notifications/{id}/read/
```

### 알림 삭제

```http
DELETE /api/notifications/{id}/
```

### 전체 알림 읽음 처리

```http
PUT /api/notifications/mark-all-read/
```

## 📊 대시보드

### 전체 통계

```http
GET /api/dashboards/overview/
```

**Query Parameters:**

- `branch` (integer): 지점 ID 필터

**Response:**

```json
{
  "total_members": 24,
  "new_members_this_month": 5,
  "total_trainers": 9,
  "today_reservations": 8,
  "monthly_revenue": 15000000
}
```

### 주간 통계

```http
GET /api/dashboards/weekly-stats/
```

**Query Parameters:**

- `branch` (integer): 지점 ID 필터
- `start_date` (date): 시작 날짜
- `end_date` (date): 종료 날짜

**Response:**

```json
{
  "new_members": 3,
  "total_reservations": 45,
  "completed_reservations": 42,
  "total_revenue": 5000000,
  "completion_rate": 93.3
}
```

### 월간 통계

```http
GET /api/dashboards/monthly-stats/
```

**Query Parameters:**

- `branch` (integer): 지점 ID 필터
- `year` (integer): 년도
- `month` (integer): 월

**Response:**

```json
{
  "total_members": 24,
  "new_members": 5,
  "total_pt_registrations": 18,
  "total_pt_revenue": 8000000,
  "total_reservations": 180,
  "completed_reservations": 165,
  "total_revenue": 15000000,
  "completion_rate": 91.7
}
```

### 매출 차트 데이터

```http
GET /api/dashboards/revenue-chart/
```

**Query Parameters:**

- `branch` (integer): 지점 ID 필터
- `months` (integer): 조회할 월 수 (기본값: 12)

**Response:**

```json
{
  "labels": ["2023년 2월", "2023년 3월", "2023년 4월"],
  "data": [12000000, 13500000, 14200000],
  "type": "line"
}
```

### 예약 차트 데이터

```http
GET /api/dashboards/reservation-chart/
```

**Query Parameters:**

- `branch` (integer): 지점 ID 필터
- `days` (integer): 조회할 일 수 (기본값: 30)

**Response:**

```json
{
  "labels": ["01/15", "01/16", "01/17"],
  "data": [8, 12, 10],
  "type": "bar"
}
```

### 트레이너 성과 데이터

```http
GET /api/dashboards/trainer-performance/
```

**Query Parameters:**

- `branch` (integer): 지점 ID 필터
- `year` (integer): 년도
- `month` (integer): 월

**Response:**

```json
[
  {
    "trainer_name": "김철수 (강남점)",
    "completed_sessions": 25,
    "total_reservations": 28,
    "completion_rate": 89.3,
    "salary": 2680000
  }
]
```

## 📈 PT 프로그램 관리

### PT 프로그램 목록

```http
GET /api/pt-programs/
```

**Query Parameters:**

- `branch` (integer): 지점 ID 필터
- `program_type` (string): 프로그램 유형 필터
- `is_active` (boolean): 활성화 여부 필터

**Response:**

```json
{
  "count": 9,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "신규 회원 PT",
      "program_type": "new",
      "sessions": 10,
      "price": "500000.00",
      "description": "신규 회원을 위한 기본 PT 프로그램",
      "is_active": true,
      "branch": {
        "id": 1,
        "name": "강남점"
      }
    }
  ]
}
```

### PT 등록 목록

```http
GET /api/pt-registrations/
```

**Query Parameters:**

- `member` (integer): 회원 ID 필터
- `trainer` (integer): 트레이너 ID 필터
- `registration_status` (string): 등록 상태 필터

**Response:**

```json
{
  "count": 18,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "member": {
        "id": 1,
        "name": "김회원1"
      },
      "pt_program": {
        "id": 1,
        "name": "신규 회원 PT"
      },
      "trainer": {
        "id": 1,
        "name": "김철수 (강남점)"
      },
      "total_sessions": 10,
      "remaining_sessions": 7,
      "total_price": "500000.00",
      "paid_amount": "500000.00",
      "registration_status": "active",
      "registration_date": "2024-01-01",
      "expiry_date": "2024-07-01"
    }
  ]
}
```

## 🔧 유틸리티 API

### 파일 업로드

```http
POST /api/upload/
```

**Request Body:**

```
Content-Type: multipart/form-data

file: [파일]
```

**Response:**

```json
{
  "url": "/media/uploads/2024/01/15/filename.jpg",
  "filename": "filename.jpg"
}
```

### 검색

```http
GET /api/search/
```

**Query Parameters:**

- `q` (string): 검색어
- `type` (string): 검색 유형 (members, trainers, reservations)

**Response:**

```json
{
  "members": [
    {
      "id": 1,
      "name": "김회원1",
      "phone": "010-4000-4000"
    }
  ],
  "trainers": [],
  "reservations": []
}
```

## ⚠️ 오류 응답

### 400 Bad Request

```json
{
  "error": "잘못된 요청입니다.",
  "details": {
    "field_name": ["이 필드는 필수입니다."]
  }
}
```

### 401 Unauthorized

```json
{
  "error": "인증이 필요합니다.",
  "detail": "자격 증명이 제공되지 않았습니다."
}
```

### 403 Forbidden

```json
{
  "error": "권한이 없습니다.",
  "detail": "이 작업을 수행할 권한이 없습니다."
}
```

### 404 Not Found

```json
{
  "error": "리소스를 찾을 수 없습니다.",
  "detail": "요청한 리소스가 존재하지 않습니다."
}
```

### 500 Internal Server Error

```json
{
  "error": "서버 오류가 발생했습니다.",
  "detail": "내부 서버 오류가 발생했습니다."
}
```

## 📝 사용 예제

### Python (requests)

```python
import requests

# 로그인
response = requests.post('http://localhost:8000/api/auth/login/', {
    'username': 'headquarters_admin',
    'password': 'password123'
})
token = response.json()['token']

# 헤더 설정
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# 회원 목록 조회
response = requests.get('http://localhost:8000/api/members/', headers=headers)
members = response.json()['results']

# 새 예약 생성
reservation_data = {
    'member': 1,
    'trainer': 1,
    'date': '2024-01-25',
    'start_time': '15:00',
    'duration': 30
}
response = requests.post('http://localhost:8000/api/reservations/',
                        json=reservation_data, headers=headers)
```

### JavaScript (fetch)

```javascript
// 로그인
const loginResponse = await fetch("http://localhost:8000/api/auth/login/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    username: "headquarters_admin",
    password: "password123",
  }),
});
const { token } = await loginResponse.json();

// 헤더 설정
const headers = {
  Authorization: `Token ${token}`,
  "Content-Type": "application/json",
};

// 회원 목록 조회
const membersResponse = await fetch("http://localhost:8000/api/members/", {
  headers,
});
const { results: members } = await membersResponse.json();

// 새 예약 생성
const reservationResponse = await fetch(
  "http://localhost:8000/api/reservations/",
  {
    method: "POST",
    headers,
    body: JSON.stringify({
      member: 1,
      trainer: 1,
      date: "2024-01-25",
      start_time: "15:00",
      duration: 30,
    }),
  }
);
```

### cURL

```bash
# 로그인
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "headquarters_admin", "password": "password123"}'

# 회원 목록 조회
curl -X GET http://localhost:8000/api/members/ \
  -H "Authorization: Token your-token-here"

# 새 예약 생성
curl -X POST http://localhost:8000/api/reservations/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "member": 1,
    "trainer": 1,
    "date": "2024-01-25",
    "start_time": "15:00",
    "duration": 30
  }'
```

## 🔄 웹훅

### 예약 상태 변경 웹훅

```http
POST /webhooks/reservation-status-changed/
```

**Request Body:**

```json
{
  "reservation_id": 1,
  "old_status": "pending",
  "new_status": "confirmed",
  "changed_by": "김철수 트레이너",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 급여 지급 웹훅

```http
POST /webhooks/salary-paid/
```

**Request Body:**

```json
{
  "salary_id": 1,
  "trainer_id": 1,
  "amount": "2680000.00",
  "payment_date": "2024-01-25",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

**API 버전**: v1.0.0  
**최종 업데이트**: 2024-01-15  
**문서 작성자**: Clamood Gym Development Team
