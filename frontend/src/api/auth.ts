import { api } from "./client";
import { User, LoginForm } from "@/types";

// 로그인 응답 타입 정의
interface LoginResponse {
  token: string;
  user_id: number;
  username: string;
  email: string;
  admin_type: string;
  branch_id: number | null;
  branch_name: string;
}

// 인증 관련 API
export const authAPI = {
  // 로그인
  login: (data: LoginForm) => api.post<LoginResponse>("/auth/login/", data),

  // 로그아웃
  logout: () => api.post("/auth/logout/"),

  // 현재 사용자 정보 조회
  getCurrentUser: () => api.get<User>("/auth/me/"),

  // 비밀번호 변경
  changePassword: (data: { old_password: string; new_password: string }) =>
    api.post("/auth/change-password/", data),
};
