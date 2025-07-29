import { api } from "./client";
import { Member, MemberForm, PaginationResponse } from "@/types";

// 회원 관련 API
export const membersAPI = {
  // 회원 목록 조회
  getMembers: (params?: {
    page?: number;
    search?: string;
    membership_status?: string;
    branch?: number;
  }) => api.get<PaginationResponse<Member>>("/members/members/", { params }),

  // 회원 상세 조회
  getMember: (id: number) => api.get<Member>(`/members/members/${id}/`),

  // 회원 등록
  createMember: (data: MemberForm) =>
    api.post<Member>("/members/members/", data),

  // 회원 수정
  updateMember: (id: number, data: Partial<MemberForm>) =>
    api.put<Member>(`/members/members/${id}/`, data),

  // 회원 삭제
  deleteMember: (id: number) => api.delete(`/members/members/${id}/`),

  // 회원 통계
  getMemberStats: () => api.get("/members/members/stats/"),
};
