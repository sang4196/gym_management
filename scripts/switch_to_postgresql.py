#!/usr/bin/env python
"""
PostgreSQL로 데이터베이스 변경 스크립트
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def switch_to_postgresql():
    """SQLite에서 PostgreSQL로 변경"""
    
    # 환경변수 설정
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clamood_gym.settings')
    
    # PostgreSQL 설정
    os.environ['DB_ENGINE'] = 'django.db.backends.postgresql'
    os.environ['DB_NAME'] = 'clamood_gym_db'
    os.environ['DB_USER'] = 'postgres'  # 실제 사용자명으로 변경
    os.environ['DB_PASSWORD'] = 'your_password'  # 실제 비밀번호로 변경
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '5432'
    
    # Django 설정
    django.setup()
    
    print("PostgreSQL로 변경 중...")
    
    # 마이그레이션 실행
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("PostgreSQL 변경 완료!")

if __name__ == '__main__':
    switch_to_postgresql() 