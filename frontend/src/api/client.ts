import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import { toast } from "react-hot-toast";

// API 기본 설정
const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000/api";

// 토큰 가져오기 함수
const getAuthToken = (): string | null => {
  return localStorage.getItem("authToken");
};

// Axios 인스턴스 생성
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: false, // CORS 문제 해결을 위해 false로 변경
});

// 요청 인터셉터
apiClient.interceptors.request.use(
  (config) => {
    // 인증 토큰 추가
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }

    // CSRF 토큰 추가 (Django)
    const csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];

    if (csrfToken) {
      config.headers["X-CSRFToken"] = csrfToken;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    // 에러 처리
    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 401:
          // 인증 실패 - 로그인 정보 삭제 후 로그인 페이지로 리다이렉트
          localStorage.removeItem("authToken");
          localStorage.removeItem("userData");
          toast.error("로그인이 필요합니다.");
          window.location.href = "/login";
          break;
        case 403:
          toast.error("접근 권한이 없습니다.");
          break;
        case 404:
          toast.error("요청한 리소스를 찾을 수 없습니다.");
          break;
        case 400:
        case 422:
          // 유효성 검사 오류 - 에러를 그대로 전달하여 컴포넌트에서 처리
          break;
        case 500:
          toast.error("서버 오류가 발생했습니다.");
          break;
        default:
          toast.error(data.error || "알 수 없는 오류가 발생했습니다.");
      }
    } else if (error.request) {
      // 네트워크 오류
      toast.error("네트워크 연결을 확인해주세요.");
    } else {
      // 기타 오류
      toast.error("오류가 발생했습니다.");
    }

    return Promise.reject(error);
  }
);

// API 메서드 래퍼
export const api = {
  get: <T = any>(url: string, config?: AxiosRequestConfig) =>
    apiClient.get<T>(url, config).then((response) => response.data),

  post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiClient.post<T>(url, data, config).then((response) => response.data),

  put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiClient.put<T>(url, data, config).then((response) => response.data),

  patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiClient.patch<T>(url, data, config).then((response) => response.data),

  delete: <T = any>(url: string, config?: AxiosRequestConfig) =>
    apiClient.delete<T>(url, config).then((response) => response.data),
};

export default apiClient;
