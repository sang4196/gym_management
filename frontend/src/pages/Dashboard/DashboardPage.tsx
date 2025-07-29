import React from 'react';
import styled from 'styled-components';
import { FaUsers, FaUserTie, FaCalendarAlt, FaMoneyBillWave } from 'react-icons/fa';

const DashboardContainer = styled.div`
  padding: 20px;
`;

const Header = styled.div`
  margin-bottom: 30px;
  
  h1 {
    font-size: 28px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
  }
  
  p {
    color: #666;
    font-size: 16px;
  }
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const StatCard = styled.div`
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  }
`;

const StatHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
`;

const StatIcon = styled.div<{ $color: string }>`
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: ${props => props.$color};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
`;

const StatInfo = styled.div`
  text-align: right;
`;

const StatValue = styled.div`
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
`;

const StatLabel = styled.div`
  font-size: 14px;
  color: #666;
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const ChartCard = styled.div`
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
`;

const ChartTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
`;

const Placeholder = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  background: #f8f9fa;
  border-radius: 10px;
  color: #666;
  font-size: 16px;
`;

const DashboardPage: React.FC = () => {
  // 임시 데이터 (실제로는 API에서 가져올 예정)
  const stats = [
    {
      label: '총 회원 수',
      value: '1,234',
      icon: <FaUsers />,
      color: '#667eea',
    },
    {
      label: '활성 회원',
      value: '987',
      icon: <FaUsers />,
      color: '#4CAF50',
    },
    {
      label: '총 트레이너',
      value: '45',
      icon: <FaUserTie />,
      color: '#FF9800',
    },
    {
      label: '이번 달 예약',
      value: '2,156',
      icon: <FaCalendarAlt />,
      color: '#9C27B0',
    },
  ];

  return (
    <DashboardContainer>
      <Header>
        <h1>대시보드</h1>
        <p>헬스장 운영 현황을 한눈에 확인하세요</p>
      </Header>
      
      <StatsGrid>
        {stats.map((stat, index) => (
          <StatCard key={index}>
            <StatHeader>
              <StatIcon $color={stat.color}>
                {stat.icon}
              </StatIcon>
              <StatInfo>
                <StatValue>{stat.value}</StatValue>
                <StatLabel>{stat.label}</StatLabel>
              </StatInfo>
            </StatHeader>
          </StatCard>
        ))}
      </StatsGrid>
      
      <ContentGrid>
        <ChartCard>
          <ChartTitle>매출 추이</ChartTitle>
          <Placeholder>
            차트가 여기에 표시됩니다
          </Placeholder>
        </ChartCard>
        
        <ChartCard>
          <ChartTitle>최근 활동</ChartTitle>
          <Placeholder>
            최근 활동 목록이 여기에 표시됩니다
          </Placeholder>
        </ChartCard>
      </ContentGrid>
    </DashboardContainer>
  );
};

export default DashboardPage; 