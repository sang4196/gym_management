import React from "react";
import styled from "styled-components";
import { useForm } from "react-hook-form";
import { FaTimes, FaSave } from "react-icons/fa";
import { Member, MemberForm, Branch } from "@/types";

interface MemberModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: MemberForm) => void;
  member?: Member | null;
  branches: Branch[];
  isLoading: boolean;
  serverErrors?: Record<string, string[]>;
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
  max-width: 600px;
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

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const FormRow = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;

  label {
    font-weight: 500;
    color: #333;
    font-size: 14px;
  }

  input,
  select,
  textarea {
    padding: 10px 12px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 14px;

    &:focus {
      outline: none;
      border-color: #007bff;
    }

    &.error {
      border-color: #dc3545;
    }
  }

  textarea {
    resize: vertical;
    min-height: 80px;
  }

  .error-message {
    color: #dc3545;
    font-size: 12px;
    margin-top: 4px;
  }
`;

const FullWidthGroup = styled(FormGroup)`
  grid-column: 1 / -1;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
`;

const Button = styled.button<{ variant?: "primary" | "secondary" }>`
  padding: 10px 20px;
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
          &:hover:not(:disabled) { background: #0056b3; }
          &:disabled { background: #6c757d; cursor: not-allowed; }
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

const MemberModal: React.FC<MemberModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  member,
  branches,
  isLoading,
  serverErrors = {},
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<MemberForm>({
    defaultValues: member
      ? {
          name: member.name,
          phone: member.phone,
          email: member.email,
          gender: member.gender,
          birth_date: member.birth_date,
          address: member.address,
          emergency_contact: member.emergency_contact,
          membership_status: member.membership_status,
          expiry_date: member.expiry_date,
          notes: member.notes,
          branch: member.branch.id,
        }
      : {
          membership_status: "active",
          branch: branches[0]?.id || 1,
        },
  });

  React.useEffect(() => {
    if (member) {
      reset({
        name: member.name,
        phone: member.phone,
        email: member.email,
        gender: member.gender,
        birth_date: member.birth_date,
        address: member.address,
        emergency_contact: member.emergency_contact,
        membership_status: member.membership_status,
        expiry_date: member.expiry_date,
        notes: member.notes,
        branch: member.branch.id,
      });
    } else {
      reset({
        membership_status: "active",
        branch: branches[0]?.id || 1,
      });
    }
  }, [member, branches, reset]);

  const handleFormSubmit = (data: MemberForm) => {
    onSubmit(data);
  };

  if (!isOpen) return null;

  return (
    <ModalOverlay onClick={onClose}>
      <ModalContent onClick={(e) => e.stopPropagation()}>
        <ModalHeader>
          <h2>{member ? "회원 정보 수정" : "새 회원 등록"}</h2>
          <button className="close-button" onClick={onClose}>
            <FaTimes />
          </button>
        </ModalHeader>

        <Form onSubmit={handleSubmit(handleFormSubmit)}>
          <FormRow>
            <FormGroup>
              <label>이름 *</label>
              <input
                type="text"
                {...register("name", { required: "이름을 입력해주세요." })}
                className={errors.name || serverErrors.name ? "error" : ""}
                placeholder="회원 이름"
              />
              {errors.name && (
                <div className="error-message">{errors.name.message}</div>
              )}
              {serverErrors.name && (
                <div className="error-message">{serverErrors.name[0]}</div>
              )}
            </FormGroup>

            <FormGroup>
              <label>전화번호 *</label>
              <input
                type="tel"
                {...register("phone", {
                  required: "전화번호를 입력해주세요.",
                  pattern: {
                    value: /^[0-9-+()\s]+$/,
                    message: "올바른 전화번호 형식을 입력해주세요.",
                  },
                })}
                className={errors.phone || serverErrors.phone ? "error" : ""}
                placeholder="010-1234-5678"
              />
              {errors.phone && (
                <div className="error-message">{errors.phone.message}</div>
              )}
              {serverErrors.phone && (
                <div className="error-message">{serverErrors.phone[0]}</div>
              )}
            </FormGroup>
          </FormRow>

          <FormRow>
            <FormGroup>
              <label>이메일</label>
              <input
                type="email"
                {...register("email", {
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: "올바른 이메일 형식을 입력해주세요.",
                  },
                })}
                className={errors.email || serverErrors.email ? "error" : ""}
                placeholder="email@example.com"
              />
              {errors.email && (
                <div className="error-message">{errors.email.message}</div>
              )}
              {serverErrors.email && (
                <div className="error-message">{serverErrors.email[0]}</div>
              )}
            </FormGroup>

            <FormGroup>
              <label>성별</label>
              <select {...register("gender")}>
                <option value="">선택하세요</option>
                <option value="M">남성</option>
                <option value="F">여성</option>
              </select>
            </FormGroup>
          </FormRow>

          <FormRow>
            <FormGroup>
              <label>생년월일</label>
              <input
                type="date"
                {...register("birth_date")}
                placeholder="YYYY-MM-DD"
              />
            </FormGroup>

            <FormGroup>
              <label>지점 *</label>
              <select
                {...register("branch", { required: "지점을 선택해주세요." })}
                className={errors.branch || serverErrors.branch ? "error" : ""}
              >
                <option value="">지점 선택</option>
                {branches.map((branch) => (
                  <option key={branch.id} value={branch.id}>
                    {branch.name}
                  </option>
                ))}
              </select>
              {errors.branch && (
                <div className="error-message">{errors.branch.message}</div>
              )}
              {serverErrors.branch && (
                <div className="error-message">{serverErrors.branch[0]}</div>
              )}
            </FormGroup>
          </FormRow>

          <FullWidthGroup>
            <label>주소</label>
            <input
              type="text"
              {...register("address")}
              placeholder="주소를 입력하세요"
            />
          </FullWidthGroup>

          <FormRow>
            <FormGroup>
              <label>비상연락처</label>
              <input
                type="tel"
                {...register("emergency_contact")}
                placeholder="010-1234-5678"
              />
            </FormGroup>

            <FormGroup>
              <label>회원 상태 *</label>
              <select
                {...register("membership_status", {
                  required: "회원 상태를 선택해주세요.",
                })}
                className={
                  errors.membership_status || serverErrors.membership_status
                    ? "error"
                    : ""
                }
              >
                <option value="active">활성</option>
                <option value="inactive">비활성</option>
                <option value="suspended">정지</option>
                <option value="expired">만료</option>
              </select>
              {errors.membership_status && (
                <div className="error-message">
                  {errors.membership_status.message}
                </div>
              )}
              {serverErrors.membership_status && (
                <div className="error-message">
                  {serverErrors.membership_status[0]}
                </div>
              )}
            </FormGroup>
          </FormRow>

          <FormRow>
            <FormGroup>
              <label>만료일</label>
              <input
                type="date"
                {...register("expiry_date")}
                placeholder="YYYY-MM-DD"
              />
            </FormGroup>
          </FormRow>

          <FullWidthGroup>
            <label>메모</label>
            <textarea
              {...register("notes")}
              placeholder="회원에 대한 추가 정보나 메모를 입력하세요"
            />
          </FullWidthGroup>

          <ButtonGroup>
            <Button type="button" onClick={onClose}>
              취소
            </Button>
            <Button type="submit" variant="primary" disabled={isLoading}>
              <FaSave />
              {isLoading ? "저장 중..." : member ? "수정" : "등록"}
            </Button>
          </ButtonGroup>
        </Form>
      </ModalContent>
    </ModalOverlay>
  );
};

export default MemberModal;
