import React, { useState, useEffect } from 'react';
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

const FilterSection = styled.div`
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  align-items: center;
  flex-wrap: wrap;
`;

const FilterSelect = styled.select`
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  font-size: 14px;
  min-width: 120px;
`;

const SearchInput = styled.input`
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  min-width: 200px;
`;

const ActionButton = styled.button`
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: #007bff;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: #0056b3;
  }

  &.secondary {
    background: #6c757d;
    
    &:hover {
      background: #545b62;
    }
  }

  &.danger {
    background: #dc3545;
    
    &:hover {
      background: #c82333;
    }
  }
`;

const NotificationList = styled.div`
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
`;

const NotificationItem = styled.div<{ isRead: boolean }>`
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
  background: ${props => props.isRead ? '#fafafa' : 'white'};

  &:hover {
    background: #f8f9fa;
  }

  &:last-child {
    border-bottom: none;
  }
`;

const NotificationHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
`;

const NotificationTitle = styled.h3<{ isRead: boolean }>`
  font-size: 16px;
  font-weight: ${props => props.isRead ? 'normal' : 'bold'};
  color: #333;
  margin: 0;
`;

const NotificationTime = styled.span`
  font-size: 12px;
  color: #666;
  white-space: nowrap;
`;

const NotificationMessage = styled.p`
  color: #666;
  font-size: 14px;
  margin: 0;
  line-height: 1.4;
`;

const NotificationType = styled.span<{ type: string }>`
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: bold;
  text-transform: uppercase;
  background: ${props => {
    switch (props.type) {
      case 'reservation_request': return '#e3f2fd';
      case 'reservation_confirmed': return '#e8f5e8';
      case 'reservation_rejected': return '#ffebee';
      case 'pt_completed': return '#fff3e0';
      case 'salary_paid': return '#f3e5f5';
      default: return '#f5f5f5';
    }
  }};
  color: ${props => {
    switch (props.type) {
      case 'reservation_request': return '#1976d2';
      case 'reservation_confirmed': return '#388e3c';
      case 'reservation_rejected': return '#d32f2f';
      case 'pt_completed': return '#f57c00';
      case 'salary_paid': return '#7b1fa2';
      default: return '#666';
    }
  }};
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #666;
  text-align: center;
`;

const EmptyIcon = styled.div`
  font-size: 48px;
  margin-bottom: 20px;
  opacity: 0.5;
`;

const Pagination = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
  padding: 20px;
`;

const PageButton = styled.button<{ active?: boolean }>`
  padding: 8px 12px;
  border: 1px solid #ddd;
  background: ${props => props.active ? '#007bff' : 'white'};
  color: ${props => props.active ? 'white' : '#333'};
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: ${props => props.active ? '#0056b3' : '#f8f9fa'};
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

interface Notification {
  id: number;
  notification_type: string;
  title: string;
  message: string;
  priority: string;
  status: string;
  kakao_sent: boolean;
  read_at: string | null;
  created_at: string;
  related_reservation?: number;
}

const NotificationsPage: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Mock data for demonstration
  const mockNotifications: Notification[] = [
    {
      id: 1,
      notification_type: 'reservation_request',
      title: '새로운 PT 예약 요청',
      message: '김철수 회원님이 2024년 1월 15일 오후 2시에 PT 예약을 요청했습니다.',
      priority: 'medium',
      status: 'pending',
      kakao_sent: true,
      read_at: null,
      created_at: '2024-01-14T10:30:00Z',
      related_reservation: 123
    },
    {
      id: 2,
      notification_type: 'reservation_confirmed',
      title: 'PT 예약이 확정되었습니다',
      message: '2024년 1월 16일 오전 10시 PT 예약이 확정되었습니다.',
      priority: 'medium',
      status: 'sent',
      kakao_sent: true,
      read_at: '2024-01-14T11:15:00Z',
      created_at: '2024-01-14T11:00:00Z',
      related_reservation: 124
    },
    {
      id: 3,
      notification_type: 'pt_completed',
      title: 'PT 세션이 완료되었습니다',
      message: '이영희 회원님의 PT 세션이 성공적으로 완료되었습니다. 수행 내역을 확인해주세요.',
      priority: 'high',
      status: 'sent',
      kakao_sent: true,
      read_at: null,
      created_at: '2024-01-14T09:45:00Z',
      related_reservation: 125
    },
    {
      id: 4,
      notification_type: 'salary_paid',
      title: '급여 지급 완료',
      message: '2024년 1월 급여가 지급되었습니다. 상세 내역을 확인해주세요.',
      priority: 'medium',
      status: 'sent',
      kakao_sent: false,
      read_at: '2024-01-14T08:30:00Z',
      created_at: '2024-01-14T08:00:00Z'
    }
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setNotifications(mockNotifications);
      setLoading(false);
      setTotalPages(1);
    }, 1000);
  }, []);

  const handleFilterChange = (value: string) => {
    setFilter(value);
    setCurrentPage(1);
  };

  const handleSearch = (value: string) => {
    setSearchTerm(value);
    setCurrentPage(1);
  };

  const markAsRead = (notificationId: number) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === notificationId 
          ? { ...notification, read_at: new Date().toISOString() }
          : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => 
      prev.map(notification => ({
        ...notification,
        read_at: notification.read_at || new Date().toISOString()
      }))
    );
  };

  const deleteNotification = (notificationId: number) => {
    setNotifications(prev => prev.filter(n => n.id !== notificationId));
  };

  const getNotificationTypeLabel = (type: string) => {
    const labels: { [key: string]: string } = {
      'reservation_request': '예약 요청',
      'reservation_confirmed': '예약 확정',
      'reservation_rejected': '예약 거절',
      'reservation_cancelled': '예약 취소',
      'reservation_reminder': '예약 알림',
      'pt_completed': 'PT 완료',
      'salary_paid': '급여 지급',
      'system': '시스템'
    };
    return labels[type] || type;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);
    
    if (diffInHours < 1) {
      return '방금 전';
    } else if (diffInHours < 24) {
      return `${Math.floor(diffInHours)}시간 전`;
    } else {
      return date.toLocaleDateString('ko-KR');
    }
  };

  const filteredNotifications = notifications.filter(notification => {
    const matchesFilter = filter === 'all' || 
      (filter === 'unread' && !notification.read_at) ||
      (filter === 'read' && notification.read_at) ||
      notification.notification_type === filter;
    
    const matchesSearch = notification.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         notification.message.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesFilter && matchesSearch;
  });

  if (loading) {
    return (
      <PageContainer>
        <Header>
          <h1>알림 관리</h1>
          <p>알림을 관리하고 설정하세요</p>
        </Header>
        <EmptyState>
          <div>로딩 중...</div>
        </EmptyState>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <Header>
        <h1>알림 관리</h1>
        <p>알림을 관리하고 설정하세요</p>
      </Header>

      <FilterSection>
        <FilterSelect 
          value={filter} 
          onChange={(e) => handleFilterChange(e.target.value)}
        >
          <option value="all">전체 알림</option>
          <option value="unread">읽지 않은 알림</option>
          <option value="read">읽은 알림</option>
          <option value="reservation_request">예약 요청</option>
          <option value="reservation_confirmed">예약 확정</option>
          <option value="pt_completed">PT 완료</option>
          <option value="salary_paid">급여 지급</option>
        </FilterSelect>

        <SearchInput
          type="text"
          placeholder="알림 검색..."
          value={searchTerm}
          onChange={(e) => handleSearch(e.target.value)}
        />

        <ActionButton onClick={markAllAsRead}>
          전체 읽음 처리
        </ActionButton>
      </FilterSection>

      {filteredNotifications.length > 0 ? (
        <>
          <NotificationList>
            {filteredNotifications.map(notification => (
              <NotificationItem 
                key={notification.id}
                isRead={!!notification.read_at}
                onClick={() => markAsRead(notification.id)}
              >
                <NotificationHeader>
                  <div style={{ flex: 1 }}>
                    <NotificationTitle isRead={!!notification.read_at}>
                      {notification.title}
                    </NotificationTitle>
                    <NotificationType type={notification.notification_type}>
                      {getNotificationTypeLabel(notification.notification_type)}
                    </NotificationType>
                  </div>
                  <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                    <NotificationTime>
                      {formatDate(notification.created_at)}
                    </NotificationTime>
                    <ActionButton 
                      className="danger"
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteNotification(notification.id);
                      }}
                    >
                      삭제
                    </ActionButton>
                  </div>
                </NotificationHeader>
                <NotificationMessage>
                  {notification.message}
                </NotificationMessage>
              </NotificationItem>
            ))}
          </NotificationList>

          <Pagination>
            <PageButton 
              disabled={currentPage === 1}
              onClick={() => setCurrentPage(prev => prev - 1)}
            >
              이전
            </PageButton>
            <span>페이지 {currentPage} / {totalPages}</span>
            <PageButton 
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage(prev => prev + 1)}
            >
              다음
            </PageButton>
          </Pagination>
        </>
      ) : (
        <EmptyState>
          <EmptyIcon>🔔</EmptyIcon>
          <h3>알림이 없습니다</h3>
          <p>새로운 알림이 도착하면 여기에 표시됩니다.</p>
        </EmptyState>
      )}
    </PageContainer>
  );
};

export default NotificationsPage; 