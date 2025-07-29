import { atom, selector, atomFamily } from "recoil";
import { User } from "@/types";

// localStorage 키
const AUTH_TOKEN_KEY = "authToken";
const USER_DATA_KEY = "userData";

// 토큰 상태
export const authTokenState = atom<string | null>({
  key: "authTokenState",
  default: localStorage.getItem(AUTH_TOKEN_KEY),
});

// 사용자 상태 (localStorage에서 초기값 복원)
const getInitialUser = (): User | null => {
  try {
    const userData = localStorage.getItem(USER_DATA_KEY);
    return userData ? JSON.parse(userData) : null;
  } catch (error) {
    console.error("Failed to parse user data from localStorage:", error);
    return null;
  }
};

export const userState = atom<User | null>({
  key: "userState",
  default: getInitialUser(),
});

// 인증 상태
export const isAuthenticatedState = selector({
  key: "isAuthenticatedState",
  get: ({ get }) => {
    const user = get(userState);
    const token = get(authTokenState);
    return user !== null && token !== null;
  },
});

// 사용자 권한 상태
export const userRoleState = selector({
  key: "userRoleState",
  get: ({ get }) => {
    const user = get(userState);
    return user?.admin_type || null;
  },
});

// 본사 어드민 여부
export const isHeadquartersAdminState = selector({
  key: "isHeadquartersAdminState",
  get: ({ get }) => {
    const user = get(userState);
    return user?.admin_type === "headquarters";
  },
});

// 지점 어드민 여부
export const isBranchAdminState = selector({
  key: "isBranchAdminState",
  get: ({ get }) => {
    const user = get(userState);
    return user?.admin_type === "branch";
  },
});

// 사용자 지점 정보
export const userBranchState = selector({
  key: "userBranchState",
  get: ({ get }) => {
    const user = get(userState);
    return user?.branch || null;
  },
});

// 인증 관련 유틸리티 함수들
export const authUtils = {
  // 로그인 정보 저장
  saveAuthData: (token: string, user: User) => {
    localStorage.setItem(AUTH_TOKEN_KEY, token);
    localStorage.setItem(USER_DATA_KEY, JSON.stringify(user));
  },

  // 로그인 정보 제거
  clearAuthData: () => {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(USER_DATA_KEY);
  },

  // 토큰 가져오기
  getToken: (): string | null => {
    return localStorage.getItem(AUTH_TOKEN_KEY);
  },

  // 사용자 정보 가져오기
  getUser: (): User | null => {
    try {
      const userData = localStorage.getItem(USER_DATA_KEY);
      return userData ? JSON.parse(userData) : null;
    } catch (error) {
      console.error("Failed to parse user data from localStorage:", error);
      return null;
    }
  },

  // 인증 상태 확인
  isAuthenticated: (): boolean => {
    const token = localStorage.getItem(AUTH_TOKEN_KEY);
    const user = authUtils.getUser();
    return token !== null && user !== null;
  },
};
