# Clamood Gym Frontend

헬스장 회원관리 시스템의 프론트엔드 애플리케이션입니다.

## 🚀 기술 스택

- **React 18** - 사용자 인터페이스 라이브러리
- **TypeScript** - 타입 안정성
- **React Router** - 클라이언트 사이드 라우팅
- **Recoil** - 상태 관리
- **Styled Components** - CSS-in-JS 스타일링
- **React Query** - 서버 상태 관리
- **Axios** - HTTP 클라이언트
- **Recharts** - 차트 라이브러리
- **React Hook Form** - 폼 관리
- **React Hot Toast** - 알림 시스템

## 📦 설치 및 실행

### 1. 의존성 설치

```bash
npm install
```

### 2. 개발 서버 실행

```bash
npm start
```

개발 서버는 `http://localhost:3000`에서 실행됩니다.

### 3. 빌드

```bash
npm run build
```

### 4. 테스트

```bash
npm test
```

## 🏗 프로젝트 구조

```
src/
├── api/                    # API 관련 파일
│   ├── client.ts          # Axios 클라이언트 설정
│   ├── auth.ts            # 인증 API
│   ├── members.ts         # 회원 API
│   ├── trainers.ts        # 트레이너 API
│   ├── reservations.ts    # 예약 API
│   └── ...
├── components/            # 재사용 가능한 컴포넌트
│   ├── Layout/           # 레이아웃 컴포넌트
│   ├── Common/           # 공통 컴포넌트
│   ├── Forms/            # 폼 컴포넌트
│   └── Charts/           # 차트 컴포넌트
├── pages/                # 페이지 컴포넌트
│   ├── Dashboard/        # 대시보드
│   ├── Members/          # 회원 관리
│   ├── Trainers/         # 트레이너 관리
│   ├── Reservations/     # 예약 관리
│   └── ...
├── hooks/                # 커스텀 훅
├── store/                # Recoil 상태 관리
├── types/                # TypeScript 타입 정의
├── utils/                # 유틸리티 함수
└── styles/               # 글로벌 스타일
```

## 🔧 주요 기능

### 1. 인증 시스템
- 로그인/로그아웃
- 권한 기반 접근 제어
- 세션 관리

### 2. 대시보드
- 실시간 통계
- 차트 및 그래프
- 최근 활동

### 3. 회원 관리
- 회원 목록 조회
- 회원 등록/수정/삭제
- 회원 검색 및 필터링
- PT 등록 관리

### 4. 트레이너 관리
- 트레이너 목록 조회
- 트레이너 등록/수정/삭제
- 일정 관리
- 인센티브 설정

### 5. 예약 관리
- 예약 목록 조회
- 예약 생성/수정/취소
- 예약 상태 관리
- PT 기록 관리

### 6. 급여 관리
- 급여 목록 조회
- 급여 계산
- 지급 처리

### 7. 알림 시스템
- 알림 목록 조회
- 알림 설정
- 실시간 알림

## 🎨 UI/UX 특징

### 디자인 시스템
- 모던하고 깔끔한 디자인
- 반응형 레이아웃
- 다크/라이트 모드 지원 (예정)

### 사용자 경험
- 직관적인 네비게이션
- 빠른 검색 및 필터링
- 드래그 앤 드롭 기능
- 키보드 단축키 지원

### 성능 최적화
- 코드 스플리팅
- 지연 로딩
- 메모이제이션
- 가상화된 리스트

## 🔐 권한 관리

### 본사 어드민
- 모든 지점의 데이터 접근
- 전체 통계 및 리포트
- 시스템 설정 관리

### 지점 어드민
- 본인 지점의 데이터만 접근
- 지점별 통계 및 리포트
- 지점 내 관리 기능

## 📱 반응형 디자인

- **데스크톱**: 1200px 이상
- **태블릿**: 768px - 1199px
- **모바일**: 767px 이하

## 🧪 테스트

### 단위 테스트
```bash
npm test
```

### E2E 테스트 (예정)
```bash
npm run test:e2e
```

## 📦 배포

### 개발 환경
```bash
npm run build:dev
```

### 운영 환경
```bash
npm run build:prod
```

## 🔧 환경 변수

`.env` 파일을 생성하여 다음 환경 변수를 설정하세요:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENV=development
```

## 📚 API 문서

백엔드 API 문서는 `../API_DOCUMENTATION.md`를 참조하세요.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 지원

- 이슈 리포트: GitHub Issues
- 이메일: support@clamood.com 