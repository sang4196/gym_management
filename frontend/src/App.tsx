import React, { useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { useRecoilValue, useSetRecoilState } from "recoil";
import {
  isAuthenticatedState,
  userState,
  authTokenState,
  authUtils,
} from "@/store/auth";
import Layout from "@/components/Layout";
import LoginPage from "@/pages/Auth/LoginPage";
import DashboardPage from "@/pages/Dashboard/DashboardPage";
import MembersPage from "@/pages/Members/MembersPage";
import TrainersPage from "@/pages/Trainers/TrainersPage";
import ReservationsPage from "@/pages/Reservations/ReservationsPage";
import SalariesPage from "@/pages/Salaries/SalariesPage";
import NotificationsPage from "@/pages/Notifications/NotificationsPage";
import SettingsPage from "@/pages/Settings/SettingsPage";
import AnalyticsPage from "@/pages/Analytics/AnalyticsPage";

// 보호된 라우트 컴포넌트
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const isAuthenticated = useRecoilValue(isAuthenticatedState);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

const App: React.FC = () => {
  const isAuthenticated = useRecoilValue(isAuthenticatedState);
  const setUser = useSetRecoilState(userState);
  const setAuthToken = useSetRecoilState(authTokenState);

  // 앱 시작 시 인증 상태 복원
  useEffect(() => {
    const token = authUtils.getToken();
    const user = authUtils.getUser();

    if (token && user) {
      setAuthToken(token);
      setUser(user);
    }
  }, [setUser, setAuthToken]);

  return (
    <div className="App">
      <Routes>
        {/* 공개 라우트 */}
        <Route
          path="/login"
          element={
            isAuthenticated ? <Navigate to="/" replace /> : <LoginPage />
          }
        />

        {/* 보호된 라우트 */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<DashboardPage />} />
          <Route path="members" element={<MembersPage />} />
          <Route path="trainers" element={<TrainersPage />} />
          <Route path="reservations" element={<ReservationsPage />} />
          <Route path="salaries" element={<SalariesPage />} />
          <Route path="notifications" element={<NotificationsPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
        </Route>

        {/* 404 페이지 */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
};

export default App;
