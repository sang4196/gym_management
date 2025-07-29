import React from "react";
import { Link, useLocation } from "react-router-dom";
import styled from "styled-components";
import {
  FaHome,
  FaUsers,
  FaUserTie,
  FaCalendarAlt,
  FaMoneyBillWave,
  FaChartBar,
  FaBell,
  FaCog,
  FaSignOutAlt,
} from "react-icons/fa";
import { useRecoilValue, useSetRecoilState } from "recoil";
import {
  userState,
  isHeadquartersAdminState,
  authTokenState,
  authUtils,
} from "@/store/auth";

const SidebarContainer = styled.div`
  width: 250px;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 0;
  position: fixed;
  left: 0;
  top: 0;
  overflow-y: auto;
`;

const Logo = styled.div`
  text-align: center;
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;

  h1 {
    font-size: 24px;
    font-weight: bold;
    margin: 0;
  }

  p {
    font-size: 12px;
    opacity: 0.8;
    margin: 5px 0 0 0;
  }
`;

const UserInfo = styled.div`
  padding: 15px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;

  .user-name {
    font-weight: bold;
    margin-bottom: 5px;
  }

  .user-role {
    font-size: 12px;
    opacity: 0.8;
  }
`;

const NavMenu = styled.nav`
  padding: 0 20px;
`;

const NavItem = styled(Link)<{ $active?: boolean }>`
  display: flex;
  align-items: center;
  padding: 12px 15px;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  margin-bottom: 5px;
  transition: all 0.3s ease;
  background: ${(props) =>
    props.$active ? "rgba(255, 255, 255, 0.2)" : "transparent"};

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateX(5px);
  }

  svg {
    margin-right: 12px;
    font-size: 16px;
  }

  span {
    font-weight: 500;
  }
`;

const LogoutButton = styled.button`
  display: flex;
  align-items: center;
  width: 100%;
  padding: 12px 15px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  svg {
    margin-right: 12px;
    font-size: 16px;
  }
`;

const Sidebar: React.FC = () => {
  const location = useLocation();
  const user = useRecoilValue(userState);
  const isHeadquartersAdmin = useRecoilValue(isHeadquartersAdminState);
  const setUser = useSetRecoilState(userState);
  const setAuthToken = useSetRecoilState(authTokenState);

  const handleLogout = () => {
    // 인증 정보 삭제
    authUtils.clearAuthData();
    setUser(null);
    setAuthToken(null);

    // 로그인 페이지로 리다이렉트
    window.location.href = "/login";
  };

  const menuItems = [
    { path: "/", icon: <FaHome />, label: "대시보드" },
    { path: "/members", icon: <FaUsers />, label: "회원 관리" },
    { path: "/trainers", icon: <FaUserTie />, label: "트레이너 관리" },
    { path: "/reservations", icon: <FaCalendarAlt />, label: "예약 관리" },
    { path: "/salaries", icon: <FaMoneyBillWave />, label: "급여 관리" },
    { path: "/notifications", icon: <FaBell />, label: "알림 관리" },
    { path: "/settings", icon: <FaCog />, label: "설정" },
  ];

  // 본사 어드민만 볼 수 있는 메뉴
  if (isHeadquartersAdmin) {
    menuItems.splice(5, 0, {
      path: "/analytics",
      icon: <FaChartBar />,
      label: "통계 분석",
    });
  }

  return (
    <SidebarContainer>
      <Logo>
        <h1>Clamood Gym</h1>
        <p>헬스장 관리 시스템</p>
      </Logo>

      {user && (
        <UserInfo>
          <div className="user-name">
            {user.first_name} {user.last_name}
          </div>
          <div className="user-role">
            {user.admin_type === "headquarters"
              ? "본사 관리자"
              : `${user.branch?.name} 지점 관리자`}
          </div>
        </UserInfo>
      )}

      <NavMenu>
        {menuItems.map((item) => (
          <NavItem
            key={item.path}
            to={item.path}
            $active={location.pathname === item.path}
          >
            {item.icon}
            <span>{item.label}</span>
          </NavItem>
        ))}

        <LogoutButton onClick={handleLogout}>
          <FaSignOutAlt />
          <span>로그아웃</span>
        </LogoutButton>
      </NavMenu>
    </SidebarContainer>
  );
};

export default Sidebar;
