import { api } from "./client";
import { Branch, PaginationResponse } from "@/types";

// 지점 관련 API
export const branchesAPI = {
  // 지점 목록 조회
  getBranches: () => api.get<PaginationResponse<Branch>>("/branches/branches/"),

  // 지점 상세 조회
  getBranch: (id: number) => api.get<Branch>(`/branches/branches/${id}/`),
};
