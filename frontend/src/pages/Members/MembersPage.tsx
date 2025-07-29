import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useQuery, useMutation, useQueryClient } from "react-query";
import { toast } from "react-hot-toast";
import {
  FaPlus,
  FaSearch,
  FaEdit,
  FaTrash,
  FaEye,
  FaFilter,
  FaDownload,
} from "react-icons/fa";
import { membersAPI } from "@/api/members";
import { branchesAPI } from "@/api/branches";
import { Member, MemberForm, Branch } from "@/types";
import MemberModal from "./MemberModal";
import MemberDetailModal from "./MemberDetailModal";

const PageContainer = styled.div`
  padding: 20px;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;

  h1 {
    font-size: 28px;
    font-weight: bold;
    color: #333;
    margin: 0;
  }

  .header-actions {
    display: flex;
    gap: 10px;
  }
`;

const StatsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const StatCard = styled.div`
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

  .stat-title {
    color: #666;
    font-size: 14px;
    margin-bottom: 8px;
  }

  .stat-value {
    font-size: 24px;
    font-weight: bold;
    color: #333;
  }

  .stat-change {
    font-size: 12px;
    color: #28a745;
    margin-top: 5px;
  }
`;

const FiltersContainer = styled.div`
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
`;

const FilterRow = styled.div`
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
`;

const FilterGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 5px;

  label {
    font-size: 12px;
    color: #666;
    font-weight: 500;
  }

  select,
  input {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 14px;
    min-width: 150px;

    &:focus {
      outline: none;
      border-color: #007bff;
    }
  }
`;

const SearchInput = styled.div`
  position: relative;
  flex: 1;
  max-width: 300px;

  input {
    width: 100%;
    padding: 8px 12px 8px 35px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 14px;

    &:focus {
      outline: none;
      border-color: #007bff;
    }
  }

  .search-icon {
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #666;
  }
`;

const Button = styled.button<{ variant?: "primary" | "secondary" | "danger" }>`
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
      case "danger":
        return `
          background: #dc3545;
          color: white;
          &:hover { background: #c82333; }
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

const TableContainer = styled.div`
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;

  th,
  td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #eee;
  }

  th {
    background: #f8f9fa;
    font-weight: 600;
    color: #333;
    font-size: 14px;
  }

  td {
    font-size: 14px;
    color: #333;
  }

  tr:hover {
    background: #f8f9fa;
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

const ActionButtons = styled.div`
  display: flex;
  gap: 5px;

  button {
    padding: 4px 8px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;

    &.view {
      background: #17a2b8;
      color: white;
      &:hover {
        background: #138496;
      }
    }

    &.edit {
      background: #ffc107;
      color: #212529;
      &:hover {
        background: #e0a800;
      }
    }

    &.delete {
      background: #dc3545;
      color: white;
      &:hover {
        background: #c82333;
      }
    }
  }
`;

const Pagination = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 20px;
  background: white;
  border-top: 1px solid #eee;

  button {
    padding: 8px 12px;
    border: 1px solid #ddd;
    background: white;
    border-radius: 5px;
    cursor: pointer;

    &:hover:not(:disabled) {
      background: #f8f9fa;
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    &.active {
      background: #007bff;
      color: white;
      border-color: #007bff;
    }
  }
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  color: #666;
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #666;

  .empty-icon {
    font-size: 48px;
    margin-bottom: 10px;
    opacity: 0.5;
  }
`;

const MembersPage: React.FC = () => {
  const [filters, setFilters] = useState({
    search: "",
    membership_status: "",
    branch: "",
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedMember, setSelectedMember] = useState<Member | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [editingMember, setEditingMember] = useState<Member | null>(null);
  const [serverErrors, setServerErrors] = useState<Record<string, string[]>>(
    {}
  );

  const queryClient = useQueryClient();

  // 지점 목록 조회
  const { data: branchesData } = useQuery({
    queryKey: ["branches"],
    queryFn: () => branchesAPI.getBranches(),
  });

  const branches = branchesData?.results || [];

  // 회원 목록 조회
  const { data: membersData, isLoading: isLoadingMembers } = useQuery({
    queryKey: ["members", filters, currentPage],
    queryFn: () =>
      membersAPI.getMembers({
        page: currentPage,
        search: filters.search || undefined,
        membership_status: filters.membership_status || undefined,
        branch: filters.branch ? parseInt(filters.branch) : undefined,
      }),
  });

  const members = membersData?.results || [];

  // 회원 통계 조회
  const { data: stats } = useQuery({
    queryKey: ["member-stats"],
    queryFn: () => membersAPI.getMemberStats(),
  });

  // 회원 생성/수정 뮤테이션
  const createMemberMutation = useMutation({
    mutationFn: (data: MemberForm) => membersAPI.createMember(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["members"] });
      queryClient.invalidateQueries({ queryKey: ["member-stats"] });
      toast.success("회원이 성공적으로 등록되었습니다.");
      setIsModalOpen(false);
      setServerErrors({});
    },
    onError: (error: any) => {
      if (error.response?.status === 400 && error.response?.data) {
        setServerErrors(error.response.data);
      } else {
        toast.error("회원 등록에 실패했습니다.");
      }
      console.error("Create member error:", error);
    },
  });

  const updateMemberMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<MemberForm> }) =>
      membersAPI.updateMember(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["members"] });
      queryClient.invalidateQueries({ queryKey: ["member-stats"] });
      toast.success("회원 정보가 성공적으로 수정되었습니다.");
      setIsModalOpen(false);
      setEditingMember(null);
      setServerErrors({});
    },
    onError: (error: any) => {
      if (error.response?.status === 400 && error.response?.data) {
        setServerErrors(error.response.data);
      } else {
        toast.error("회원 정보 수정에 실패했습니다.");
      }
      console.error("Update member error:", error);
    },
  });

  // 회원 삭제 뮤테이션
  const deleteMemberMutation = useMutation({
    mutationFn: (id: number) => membersAPI.deleteMember(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["members"] });
      queryClient.invalidateQueries({ queryKey: ["member-stats"] });
      toast.success("회원이 성공적으로 삭제되었습니다.");
    },
    onError: (error: any) => {
      toast.error("회원 삭제에 실패했습니다.");
      console.error("Delete member error:", error);
    },
  });

  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
    setCurrentPage(1);
  };

  const handleCreateMember = () => {
    setEditingMember(null);
    setServerErrors({});
    setIsModalOpen(true);
  };

  const handleEditMember = (member: Member) => {
    setEditingMember(member);
    setServerErrors({});
    setIsModalOpen(true);
  };

  const handleViewMember = (member: Member) => {
    setSelectedMember(member);
    setIsDetailModalOpen(true);
  };

  const handleDeleteMember = (member: Member) => {
    if (window.confirm(`정말로 ${member.name} 회원을 삭제하시겠습니까?`)) {
      deleteMemberMutation.mutate(member.id);
    }
  };

  const handleSubmitMember = (data: MemberForm) => {
    if (editingMember) {
      updateMemberMutation.mutate({ id: editingMember.id, data });
    } else {
      createMemberMutation.mutate(data);
    }
  };

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

  return (
    <PageContainer>
      <Header>
        <h1>회원 관리</h1>
        <div className="header-actions">
          <Button variant="secondary">
            <FaDownload />
            내보내기
          </Button>
          <Button variant="primary" onClick={handleCreateMember}>
            <FaPlus />
            회원 등록
          </Button>
        </div>
      </Header>

      {/* 통계 카드 */}
      <StatsContainer>
        <StatCard>
          <div className="stat-title">총 회원 수</div>
          <div className="stat-value">{stats?.total_members || 0}</div>
        </StatCard>
        <StatCard>
          <div className="stat-title">활성 회원</div>
          <div className="stat-value">{stats?.active_members || 0}</div>
        </StatCard>
        <StatCard>
          <div className="stat-title">만료 회원</div>
          <div className="stat-value">{stats?.expired_members || 0}</div>
        </StatCard>
        <StatCard>
          <div className="stat-title">이번 달 신규</div>
          <div className="stat-value">{stats?.monthly_registrations || 0}</div>
        </StatCard>
      </StatsContainer>

      {/* 필터 */}
      <FiltersContainer>
        <FilterRow>
          <SearchInput>
            <FaSearch className="search-icon" />
            <input
              type="text"
              placeholder="이름, 전화번호로 검색..."
              value={filters.search}
              onChange={(e) => handleFilterChange("search", e.target.value)}
            />
          </SearchInput>

          <FilterGroup>
            <label>회원 상태</label>
            <select
              value={filters.membership_status}
              onChange={(e) =>
                handleFilterChange("membership_status", e.target.value)
              }
            >
              <option value="">전체</option>
              <option value="active">활성</option>
              <option value="inactive">비활성</option>
              <option value="suspended">정지</option>
              <option value="expired">만료</option>
            </select>
          </FilterGroup>

          <FilterGroup>
            <label>지점</label>
            <select
              value={filters.branch}
              onChange={(e) => handleFilterChange("branch", e.target.value)}
            >
              <option value="">전체</option>
              {branches.map((branch: Branch) => (
                <option key={branch.id} value={branch.id}>
                  {branch.name}
                </option>
              ))}
            </select>
          </FilterGroup>
        </FilterRow>
      </FiltersContainer>

      {/* 회원 목록 테이블 */}
      <TableContainer>
        {isLoadingMembers ? (
          <LoadingSpinner>로딩 중...</LoadingSpinner>
        ) : members.length === 0 ? (
          <EmptyState>
            <div className="empty-icon">👥</div>
            <div>등록된 회원이 없습니다.</div>
            <Button
              variant="primary"
              onClick={handleCreateMember}
              style={{ marginTop: "10px" }}
            >
              <FaPlus />첫 회원 등록하기
            </Button>
          </EmptyState>
        ) : (
          <>
            <Table>
              <thead>
                <tr>
                  <th>이름</th>
                  <th>전화번호</th>
                  <th>성별</th>
                  <th>지점</th>
                  <th>상태</th>
                  <th>가입일</th>
                  <th>만료일</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                {members.map((member: Member) => (
                  <tr key={member.id}>
                    <td>{member.name}</td>
                    <td>{member.phone}</td>
                    <td>{getGenderText(member.gender)}</td>
                    <td>{member.branch_name}</td>
                    <td>
                      <StatusBadge status={member.membership_status}>
                        {getStatusText(member.membership_status)}
                      </StatusBadge>
                    </td>
                    <td>{formatDate(member.registration_date)}</td>
                    <td>
                      {member.expiry_date
                        ? formatDate(member.expiry_date)
                        : "-"}
                    </td>
                    <td>
                      <ActionButtons>
                        <button
                          className="view"
                          onClick={() => handleViewMember(member)}
                          title="상세보기"
                        >
                          <FaEye />
                        </button>
                        <button
                          className="edit"
                          onClick={() => handleEditMember(member)}
                          title="수정"
                        >
                          <FaEdit />
                        </button>
                        <button
                          className="delete"
                          onClick={() => handleDeleteMember(member)}
                          title="삭제"
                        >
                          <FaTrash />
                        </button>
                      </ActionButtons>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>

            {/* 페이지네이션 */}
            {membersData && membersData.count > 0 && (
              <Pagination>
                <button
                  onClick={() =>
                    setCurrentPage((prev) => Math.max(1, prev - 1))
                  }
                  disabled={currentPage === 1}
                >
                  이전
                </button>

                {Array.from(
                  { length: Math.ceil(membersData.count / 10) },
                  (_, i) => i + 1
                )
                  .slice(Math.max(0, currentPage - 3), currentPage + 2)
                  .map((page) => (
                    <button
                      key={page}
                      onClick={() => setCurrentPage(page)}
                      className={currentPage === page ? "active" : ""}
                    >
                      {page}
                    </button>
                  ))}

                <button
                  onClick={() => setCurrentPage((prev) => prev + 1)}
                  disabled={!membersData.next}
                >
                  다음
                </button>
              </Pagination>
            )}
          </>
        )}
      </TableContainer>

      {/* 회원 등록/수정 모달 */}
      {isModalOpen && (
        <MemberModal
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setEditingMember(null);
            setServerErrors({});
          }}
          onSubmit={handleSubmitMember}
          member={editingMember}
          branches={branches}
          isLoading={
            createMemberMutation.isLoading || updateMemberMutation.isLoading
          }
          serverErrors={serverErrors}
        />
      )}

      {/* 회원 상세보기 모달 */}
      {isDetailModalOpen && selectedMember && (
        <MemberDetailModal
          isOpen={isDetailModalOpen}
          onClose={() => {
            setIsDetailModalOpen(false);
            setSelectedMember(null);
          }}
          member={selectedMember}
        />
      )}
    </PageContainer>
  );
};

export default MembersPage;
