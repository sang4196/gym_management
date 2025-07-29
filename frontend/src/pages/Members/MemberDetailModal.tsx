import React from "react";
import styled from "styled-components";
import {
  FaTimes,
  FaEdit,
  FaPhone,
  FaEnvelope,
  FaMapMarkerAlt,
  FaCalendarAlt,
  FaUser,
} from "react-icons/fa";
import { Member } from "@/types";

interface MemberDetailModalProps {
  isOpen: boolean;
  onClose: () => void;
  member: Member;
  onEdit?: () => void;
}

const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background: white;
  border-radius: 10px;
  padding: 30px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
`;

const ModalHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;

  h2 {
    margin: 0;
    font-size: 24px;
    color: #333;
  }

  .header-actions {
    display: flex;
    gap: 10px;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #666;
    padding: 5px;

    &:hover {
      color: #333;
    }
  }
`;

const Button = styled.button<{ variant?: "primary" | "secondary" }>`
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s;

  ${({ variant }) => {
    switch (variant) {
      case "primary":
        return `
          background: #007bff;
          color: white;
          &:hover { background: #0056b3; }
        `;
      case "secondary":
        return `
          background: #6c757d;
          color: white;
          &:hover { background: #545b62; }
        `;
      default:
        return `
          background: #f8f9fa;
          color: #333;
          border: 1px solid #ddd;
          &:hover { background: #e2e6ea; }
        `;
    }
  }}
`;

const MemberInfo = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const InfoSection = styled.div`
  h3 {
    font-size: 18px;
    color: #333;
    margin-bottom: 15px;
    padding-bottom: 8px;
    border-bottom: 2px solid #007bff;
  }
`;

const InfoRow = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;

  .icon {
    color: #666;
    width: 16px;
    flex-shrink: 0;
  }

  .label {
    font-weight: 500;
    color: #666;
    min-width: 80px;
    font-size: 14px;
  }

  .value {
    color: #333;
    font-size: 14px;
    flex: 1;
  }
`;

const StatusBadge = styled.span<{ status: string }>`
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;

  ${({ status }) => {
    switch (status) {
      case "active":
        return "background: #d4edda; color: #155724;";
      case "inactive":
        return "background: #f8d7da; color: #721c24;";
      case "suspended":
        return "background: #fff3cd; color: #856404;";
      case "expired":
        return "background: #d1ecf1; color: #0c5460;";
      default:
        return "background: #e2e3e5; color: #383d41;";
    }
  }}
`;

const PTRegistrations = styled.div`
  margin-top: 30px;

  h3 {
    font-size: 18px;
    color: #333;
    margin-bottom: 15px;
    padding-bottom: 8px;
    border-bottom: 2px solid #007bff;
  }
`;

const PTRegistrationCard = styled.div`
  background: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;

  .pt-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }

  .pt-name {
    font-weight: 600;
    color: #333;
  }

  .pt-status {
    font-size: 12px;
    padding: 2px 6px;
    border-radius: 8px;
    background: #007bff;
    color: white;
  }

  .pt-details {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    font-size: 13px;
    color: #666;
  }
`;

const Notes = styled.div`
  margin-top: 20px;

  .notes-content {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 15px;
    font-size: 14px;
    color: #333;
    line-height: 1.5;
    min-height: 60px;
  }
`;

const MemberDetailModal: React.FC<MemberDetailModalProps> = ({
  isOpen,
  onClose,
  member,
  onEdit,
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("ko-KR");
  };

  const getStatusText = (status: string) => {
    const statusMap: Record<string, string> = {
      active: "활성",
      inactive: "비활성",
      suspended: "정지",
      expired: "만료",
    };
    return statusMap[status] || status;
  };

  const getGenderText = (gender: string) => {
    return gender === "M" ? "남성" : "여성";
  };

  if (!isOpen) return null;

  return (
    <ModalOverlay onClick={onClose}>
      <ModalContent onClick={(e) => e.stopPropagation()}>
        <ModalHeader>
          <h2>회원 상세 정보</h2>
          <div className="header-actions">
            {onEdit && (
              <Button variant="primary" onClick={onEdit}>
                <FaEdit />
                수정
              </Button>
            )}
            <button className="close-button" onClick={onClose}>
              <FaTimes />
            </button>
          </div>
        </ModalHeader>

        <MemberInfo>
          <InfoSection>
            <h3>기본 정보</h3>

            <InfoRow>
              <FaUser className="icon" />
              <span className="label">이름:</span>
              <span className="value">{member.name}</span>
            </InfoRow>

            <InfoRow>
              <FaPhone className="icon" />
              <span className="label">전화번호:</span>
              <span className="value">{member.phone}</span>
            </InfoRow>

            {member.email && (
              <InfoRow>
                <FaEnvelope className="icon" />
                <span className="label">이메일:</span>
                <span className="value">{member.email}</span>
              </InfoRow>
            )}

            <InfoRow>
              <span className="label">성별:</span>
              <span className="value">{getGenderText(member.gender)}</span>
            </InfoRow>

            {member.birth_date && (
              <InfoRow>
                <FaCalendarAlt className="icon" />
                <span className="label">생년월일:</span>
                <span className="value">{formatDate(member.birth_date)}</span>
              </InfoRow>
            )}

            <InfoRow>
              <span className="label">지점:</span>
              <span className="value">{member.branch_name}</span>
            </InfoRow>
          </InfoSection>

          <InfoSection>
            <h3>회원 정보</h3>

            <InfoRow>
              <span className="label">상태:</span>
              <StatusBadge status={member.membership_status}>
                {getStatusText(member.membership_status)}
              </StatusBadge>
            </InfoRow>

            <InfoRow>
              <FaCalendarAlt className="icon" />
              <span className="label">가입일:</span>
              <span className="value">
                {formatDate(member.registration_date)}
              </span>
            </InfoRow>

            {member.expiry_date && (
              <InfoRow>
                <FaCalendarAlt className="icon" />
                <span className="label">만료일:</span>
                <span className="value">{formatDate(member.expiry_date)}</span>
              </InfoRow>
            )}

            {member.address && (
              <InfoRow>
                <FaMapMarkerAlt className="icon" />
                <span className="label">주소:</span>
                <span className="value">{member.address}</span>
              </InfoRow>
            )}

            {member.emergency_contact && (
              <InfoRow>
                <FaPhone className="icon" />
                <span className="label">비상연락처:</span>
                <span className="value">{member.emergency_contact}</span>
              </InfoRow>
            )}
          </InfoSection>
        </MemberInfo>

        {/* PT 등록 정보 */}
        {member.pt_registrations && member.pt_registrations.length > 0 && (
          <PTRegistrations>
            <h3>PT 등록 정보</h3>
            {member.pt_registrations.map((registration) => (
              <PTRegistrationCard key={registration.id}>
                <div className="pt-header">
                  <span className="pt-name">
                    {registration.pt_program.name}
                  </span>
                  <span className="pt-status">
                    {registration.registration_status}
                  </span>
                </div>
                <div className="pt-details">
                  <div>총 세션: {registration.total_sessions}회</div>
                  <div>남은 세션: {registration.remaining_sessions}회</div>
                  <div>
                    총 금액: {Number(registration.total_price).toLocaleString()}
                    원
                  </div>
                  <div>
                    결제 금액:{" "}
                    {Number(registration.paid_amount).toLocaleString()}원
                  </div>
                </div>
              </PTRegistrationCard>
            ))}
          </PTRegistrations>
        )}

        {/* 메모 */}
        {member.notes && (
          <Notes>
            <h3>메모</h3>
            <div className="notes-content">{member.notes}</div>
          </Notes>
        )}
      </ModalContent>
    </ModalOverlay>
  );
};

export default MemberDetailModal;
