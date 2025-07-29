#!/usr/bin/env python
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clamood_gym.settings')
django.setup()

from apps.branches.models import Branch, BranchAdmin

def create_user():
    # 지점 생성
    branch, _ = Branch.objects.get_or_create(
        name='강남점',
        defaults={
            'address': '서울특별시 강남구 테헤란로 123',
            'phone': '02-1234-5678',
            'email': 'gangnam@clamood.com'
        }
    )
    
    # 사용자 생성
    user, created = BranchAdmin.objects.get_or_create(
        username='headquarters_admin',
        defaults={
            'email': 'headquarters@clamood.com',
            'first_name': '본사',
            'last_name': '관리자',
            'admin_type': 'headquarters',
            'phone': '010-0000-0000',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        user.set_password('password123')
        user.save()
        print("✅ 사용자 생성 완료!")
        print(f"Username: {user.username}")
        print(f"Password: password123")
    else:
        user.set_password('password123')
        user.save()
        print("✅ 비밀번호 재설정 완료!")
        print(f"Username: {user.username}")
        print(f"Password: password123")

if __name__ == '__main__':
    create_user() 