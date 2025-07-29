// API 응답 기본 타입
export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  error?: string;
}

// 사용자 관련 타입
export interface User {
  id: number;
  username: string;
  email: string;
  admin_type: "headquarters" | "branch";
  branch?: Branch;
  first_name: string;
  last_name: string;
  phone: string;
}

// 지점 관련 타입
export interface Branch {
  id: number;
  name: string;
  address: string;
  phone: string;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// 회원 관련 타입
export interface Member {
  id: number;
  name: string;
  phone: string;
  email: string;
  gender: "M" | "F";
  birth_date?: string;
  address: string;
  emergency_contact: string;
  membership_status: "active" | "inactive" | "suspended" | "expired";
  registration_date: string;
  expiry_date?: string;
  notes: string;
  branch: Branch;
  branch_name: string;
  pt_registrations?: MemberPTRegistration[];
  created_at: string;
  updated_at: string;
}

// PT 프로그램 타입
export interface PTProgram {
  id: number;
  name: string;
  program_type: "new" | "long_term" | "short_term";
  sessions: number;
  price: string;
  description: string;
  is_active: boolean;
  branch: Branch;
  created_at: string;
  updated_at: string;
}

// PT 등록 타입
export interface MemberPTRegistration {
  id: number;
  member: Member;
  pt_program: PTProgram;
  trainer?: Trainer;
  total_sessions: number;
  remaining_sessions: number;
  total_price: string;
  paid_amount: string;
  registration_status: "active" | "completed" | "cancelled" | "expired";
  registration_date: string;
  expiry_date?: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

// 트레이너 관련 타입
export interface Trainer {
  id: number;
  name: string;
  phone: string;
  email: string;
  gender: "M" | "F";
  birth_date?: string;
  address: string;
  emergency_contact: string;
  employment_status: "active" | "inactive" | "resigned";
  hire_date: string;
  base_salary: string;
  kakao_id: string;
  profile_image?: string;
  specialties: string;
  certifications: string;
  experience_years: number;
  notes: string;
  branch: Branch;
  created_at: string;
  updated_at: string;
}

// 트레이너 일정 타입
export interface TrainerSchedule {
  id: number;
  trainer: Trainer;
  day_of_week: number;
  start_time: string;
  end_time: string;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

// 예약 관련 타입
export interface Reservation {
  id: number;
  member: Member;
  trainer: Trainer;
  pt_registration?: MemberPTRegistration;
  date: string;
  start_time: string;
  end_time: string;
  duration: number;
  reservation_status:
    | "pending"
    | "confirmed"
    | "rejected"
    | "cancelled"
    | "completed"
    | "no_show";
  repeat_type: "none" | "daily" | "weekly" | "monthly";
  repeat_end_date?: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

// PT 기록 타입
export interface PTRecord {
  id: number;
  reservation: Reservation;
  trainer: Trainer;
  member: Member;
  workout_date: string;
  workout_time: string;
  duration: number;
  content: string;
  member_condition: string;
  trainer_notes: string;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

// 급여 관련 타입
export interface Salary {
  id: number;
  trainer: Trainer;
  year: number;
  month: number;
  base_salary: string;
  incentive_amount: string;
  additional_revenue: string;
  other_costs: string;
  total_salary: string;
  payment_status: "pending" | "paid" | "cancelled";
  payment_date?: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

// 알림 관련 타입
export interface Notification {
  id: number;
  notification_type: string;
  recipient_type: string;
  recipient_id: number;
  title: string;
  message: string;
  priority: "low" | "medium" | "high" | "urgent";
  status: "pending" | "sent" | "failed" | "read";
  kakao_sent: boolean;
  kakao_sent_at?: string;
  read_at?: string;
  related_reservation?: Reservation;
  created_at: string;
  updated_at: string;
}

// 대시보드 통계 타입
export interface DashboardOverview {
  total_members: number;
  active_members: number;
  total_trainers: number;
  monthly_reservations: {
    confirmed: number;
    completed: number;
    total: number;
  };
  monthly_revenue: {
    pt_revenue: number;
    membership_revenue: number;
    additional_revenue: number;
    total_revenue: number;
  };
  monthly_salary: {
    base_salary: number;
    incentive: number;
    additional_revenue: number;
    other_costs: number;
    total_salary: number;
  };
}

// 차트 데이터 타입
export interface ChartData {
  period: string;
  total_revenue: number;
  pt_revenue: number;
  membership_revenue: number;
}

// 필터 옵션 타입
export interface FilterOptions {
  branch?: number;
  date_from?: string;
  date_to?: string;
  status?: string;
  search?: string;
}

// 페이지네이션 타입
export interface PaginationResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

// 폼 데이터 타입
export interface LoginForm {
  username: string;
  password: string;
}

export interface MemberForm {
  name: string;
  phone: string;
  email: string;
  gender: "M" | "F";
  birth_date?: string;
  address: string;
  emergency_contact: string;
  membership_status: "active" | "inactive" | "suspended" | "expired";
  expiry_date?: string;
  notes: string;
  branch: number;
}

export interface ReservationForm {
  member: number;
  trainer: number;
  date: string;
  start_time: string;
  duration: number;
  pt_registration?: number;
  repeat_type: "none" | "daily" | "weekly" | "monthly";
  repeat_end_date?: string;
  notes: string;
}
