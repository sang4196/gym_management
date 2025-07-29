import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSetRecoilState } from "recoil";
import styled from "styled-components";
import { useForm } from "react-hook-form";
import { toast } from "react-hot-toast";
import { FaUser, FaLock, FaEye, FaEyeSlash } from "react-icons/fa";
import { userState, authTokenState, authUtils } from "@/store/auth";
import { authAPI } from "@/api/auth";
import { LoginForm } from "@/types";
import { User } from "@/types";

const LoginContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const LoginCard = styled.div`
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
  animation: fadeIn 0.5s ease-out;
`;

const Logo = styled.div`
  text-align: center;
  margin-bottom: 30px;

  h1 {
    font-size: 28px;
    font-weight: bold;
    color: #333;
    margin-bottom: 5px;
  }

  p {
    color: #666;
    font-size: 14px;
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const InputGroup = styled.div`
  position: relative;
`;

const Input = styled.input<{ $hasError?: boolean }>`
  width: 100%;
  padding: 15px 15px 15px 45px;
  border: 2px solid ${(props) => (props.$hasError ? "#e74c3c" : "#e1e5e9")};
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: #f8f9fa;

  &:focus {
    outline: none;
    border-color: #667eea;
    background: white;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  &::placeholder {
    color: #999;
  }
`;

const InputIcon = styled.div`
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 16px;
`;

const PasswordToggle = styled.button`
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 16px;

  &:hover {
    color: #667eea;
  }
`;

const ErrorMessage = styled.span`
  color: #e74c3c;
  font-size: 12px;
  margin-top: 5px;
  display: block;
`;

const LoginButton = styled.button`
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const setUser = useSetRecoilState(userState);
  const setAuthToken = useSetRecoilState(authTokenState);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>();

  const onSubmit = async (data: LoginForm) => {
    setIsLoading(true);

    try {
      const response = await authAPI.login(data);

      // 백엔드 응답 형식에 맞게 처리
      if (response.token) {
        // 사용자 정보를 User 타입에 맞게 변환
        const user: User = {
          id: response.user_id,
          username: response.username,
          email: response.email,
          admin_type: response.admin_type as "headquarters" | "branch",
          first_name: response.username, // 임시로 username 사용
          last_name: "", // 빈 문자열
          phone: "", // 빈 문자열
          branch: response.branch_id
            ? {
                id: response.branch_id,
                name: response.branch_name,
                address: "",
                phone: "",
                email: "",
                is_active: true,
                created_at: "",
                updated_at: "",
              }
            : undefined,
        };

        // 인증 정보를 localStorage와 Recoil 상태에 저장
        authUtils.saveAuthData(response.token, user);
        setAuthToken(response.token);
        setUser(user);

        toast.success("로그인되었습니다.");
        navigate("/");
      }
    } catch (error) {
      console.error("Login error:", error);
      toast.error("로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <LoginContainer>
      <LoginCard>
        <Logo>
          <h1>Clamood Gym</h1>
          <p>헬스장 관리 시스템</p>
        </Logo>

        <Form onSubmit={handleSubmit(onSubmit)}>
          <InputGroup>
            <InputIcon>
              <FaUser />
            </InputIcon>
            <Input
              type="text"
              placeholder="아이디"
              $hasError={!!errors.username}
              {...register("username", {
                required: "아이디를 입력해주세요.",
              })}
            />
            {errors.username && (
              <ErrorMessage>{errors.username.message}</ErrorMessage>
            )}
          </InputGroup>

          <InputGroup>
            <InputIcon>
              <FaLock />
            </InputIcon>
            <Input
              type={showPassword ? "text" : "password"}
              placeholder="비밀번호"
              $hasError={!!errors.password}
              {...register("password", {
                required: "비밀번호를 입력해주세요.",
              })}
            />
            <PasswordToggle
              type="button"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </PasswordToggle>
            {errors.password && (
              <ErrorMessage>{errors.password.message}</ErrorMessage>
            )}
          </InputGroup>

          <LoginButton type="submit" disabled={isLoading}>
            {isLoading ? "로그인 중..." : "로그인"}
          </LoginButton>
        </Form>
      </LoginCard>
    </LoginContainer>
  );
};

export default LoginPage;
