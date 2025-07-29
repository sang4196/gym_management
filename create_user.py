#!/usr/bin/env python
"""
사용자 생성 스크립트
"""

import os
import sys
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clamood_gym.settings')
django.setup()

from apps.branches.models import Branch, BranchAdmin

def create_test_user():
    """테스트 사용자 생성"""
    print("테스트 사용자 생성 중...")
    
    # 지점 생성 (없는 경우)
    branch, created = Branch.objects.get_or_create(
        name='강남점',
        defaults={
            'address': '서울특별시 강남구 테헤란로 123',
            'phone': '02-1234-5678',
            'email': 'gangnam@clamood.com'
        }
    )
    if created:
        print(f"지점 생성: {branch.name}")
    
    # 본사 어드민 생성
    admin, created = BranchAdmin.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@clamood.com',
            'first_name': '관리자',
            'last_name': '계정',
            'admin_type': 'headquarters',
            'phone': '010-0000-0000',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin.set_password('password123')
        admin.save()
        print("본사 어드민 생성 완료")
        print(f"Username: {admin.username}")
        print(f"Password: password123")
    else:
        print("이미 존재하는 사용자입니다.")
        print(f"Username: {admin.username}")
        print("비밀번호를 재설정합니다...")
        admin.set_password('password123')
        admin.save()
        print("비밀번호 재설정 완료")

if __name__ == '__main__':
    create_test_user() 