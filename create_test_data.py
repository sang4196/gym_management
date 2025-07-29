#!/usr/bin/env python
"""
간단한 테스트 데이터 생성 스크립트
"""

import os
import sys
import django
from datetime import date

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clamood_gym.settings')
django.setup()

from apps.branches.models import Branch
from apps.members.models import Member

def create_test_data():
    """테스트 데이터 생성"""
    print("테스트 데이터 생성 중...")
    
    # 1. 지점 생성
    branch, created = Branch.objects.get_or_create(
        name='강남점',
        defaults={
            'address': '서울특별시 강남구 테헤란로 123',
            'phone': '02-1234-5678',
            'email': 'gangnam@clamood.com',
            'is_active': True
        }
    )
    if created:
        print(f"지점 생성: {branch.name}")
    
    # 2. 회원 생성
    member, created = Member.objects.get_or_create(
        name='김테스트',
        defaults={
            'phone': '010-1234-5678',
            'email': 'test@example.com',
            'gender': 'M',
            'birth_date': date(1990, 1, 1),
            'address': '서울시 강남구',
            'emergency_contact': '010-9876-5432',
            'membership_status': 'active',
            'branch': branch
        }
    )
    if created:
        print(f"회원 생성: {member.name}")
    
    member2, created = Member.objects.get_or_create(
        name='이테스트',
        defaults={
            'phone': '010-2345-6789',
            'email': 'test2@example.com',
            'gender': 'F',
            'birth_date': date(1995, 5, 15),
            'address': '서울시 강남구',
            'emergency_contact': '010-8765-4321',
            'membership_status': 'active',
            'branch': branch
        }
    )
    if created:
        print(f"회원 생성: {member2.name}")
    
    print("테스트 데이터 생성 완료!")

if __name__ == '__main__':
    create_test_data() 