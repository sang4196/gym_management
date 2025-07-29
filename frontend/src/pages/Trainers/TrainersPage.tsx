import React from 'react';
import styled from 'styled-components';

const PageContainer = styled.div`
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

const Placeholder = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  color: #666;
  font-size: 18px;
`;

const TrainersPage: React.FC = () => {
  return (
    <PageContainer>
      <Header>
        <h1>트레이너 관리</h1>
        <p>트레이너 정보와 일정을 관리하세요</p>
      </Header>
      
      <Placeholder>
        트레이너 관리 기능이 여기에 구현됩니다
      </Placeholder>
    </PageContainer>
  );
};

export default TrainersPage; 