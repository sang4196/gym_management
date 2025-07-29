from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time

from apps.branches.models import Branch, BranchAdmin
from apps.members.models import Member, PTProgram, MemberPTRegistration
from apps.trainers.models import Trainer, TrainerIncentive, TrainerSchedule
from apps.reservations.models import Reservation
from apps.salaries.models import Salary, BranchRevenue
from apps.notifications.models import NotificationTemplate

class Command(BaseCommand):
    help = '샘플 데이터 생성'

    def handle(self, *args, **options):
        self.stdout.write("샘플 데이터 생성 시작...")
        
        # 1. 지점 생성
        branch1, created = Branch.objects.get_or_create(
            name="강남점",
            defaults={
                'address': "서울시 강남구 테헤란로 123",
                'phone': "02-1234-5678",
                'email': "gangnam@clamood.com"
            }
        )
        
        branch2, created = Branch.objects.get_or_create(
            name="홍대점",
            defaults={
                'address': "서울시 마포구 홍대로 456",
                'phone': "02-2345-6789",
                'email': "hongdae@clamood.com"
            }
        )
        
        self.stdout.write(f"지점 생성 완료: {branch1.name}, {branch2.name}")
        
        # 2. 트레이너 생성
        trainer1, created = Trainer.objects.get_or_create(
            name="김트레이너",
            defaults={
                'branch': branch1,
                'phone': "010-1111-2222",
                'email': "trainer1@clamood.com",
                'hire_date': date(2023, 1, 1),
                'base_salary': 3000000,
                'experience_years': 5,
                'specialties': "웨이트 트레이닝, 유산소 운동"
            }
        )
        
        trainer2, created = Trainer.objects.get_or_create(
            name="이트레이너",
            defaults={
                'branch': branch2,
                'phone': "010-2222-3333",
                'email': "trainer2@clamood.com",
                'hire_date': date(2023, 2, 1),
                'base_salary': 2800000,
                'experience_years': 3,
                'specialties': "요가, 필라테스"
            }
        )
        
        self.stdout.write(f"트레이너 생성 완료: {trainer1.name}, {trainer2.name}")
        
        # 3. 트레이너 인센티브 설정
        TrainerIncentive.objects.get_or_create(
            trainer=trainer1,
            defaults={
                'incentive_type': 'fixed',
                'fixed_amount': 50000
            }
        )
        
        TrainerIncentive.objects.get_or_create(
            trainer=trainer2,
            defaults={
                'incentive_type': 'percentage',
                'percentage_rate': 10.0
            }
        )
        
        self.stdout.write("트레이너 인센티브 설정 완료")
        
        # 4. 트레이너 일정 설정
        for day in range(7):  # 월~일
            TrainerSchedule.objects.get_or_create(
                trainer=trainer1,
                day_of_week=day,
                defaults={
                    'start_time': time(9, 0),
                    'end_time': time(18, 0)
                }
            )
            
            TrainerSchedule.objects.get_or_create(
                trainer=trainer2,
                day_of_week=day,
                defaults={
                    'start_time': time(10, 0),
                    'end_time': time(19, 0)
                }
            )
        
        self.stdout.write("트레이너 일정 설정 완료")
        
        # 5. PT 프로그램 생성
        program1, created = PTProgram.objects.get_or_create(
            name="신규 PT 10회",
            defaults={
                'branch': branch1,
                'program_type': 'new',
                'sessions': 10,
                'price': 500000,
                'description': "신규 회원을 위한 기본 PT 프로그램"
            }
        )
        
        program2, created = PTProgram.objects.get_or_create(
            name="장기 PT 30회",
            defaults={
                'branch': branch1,
                'program_type': 'long_term',
                'sessions': 30,
                'price': 1200000,
                'description': "장기 회원을 위한 종합 PT 프로그램"
            }
        )
        
        self.stdout.write(f"PT 프로그램 생성 완료: {program1.name}, {program2.name}")
        
        # 6. 회원 생성
        member1, created = Member.objects.get_or_create(
            name="박회원",
            defaults={
                'branch': branch1,
                'phone': "010-3333-4444",
                'email': "member1@example.com",
                'gender': 'M',
                'membership_status': 'active'
            }
        )
        
        member2, created = Member.objects.get_or_create(
            name="최회원",
            defaults={
                'branch': branch2,
                'phone': "010-4444-5555",
                'email': "member2@example.com",
                'gender': 'F',
                'membership_status': 'active'
            }
        )
        
        self.stdout.write(f"회원 생성 완료: {member1.name}, {member2.name}")
        
        # 7. PT 등록
        registration1, created = MemberPTRegistration.objects.get_or_create(
            member=member1,
            pt_program=program1,
            defaults={
                'trainer': trainer1,
                'total_sessions': 10,
                'remaining_sessions': 8,
                'total_price': 500000,
                'paid_amount': 500000,
                'registration_status': 'active'
            }
        )
        
        self.stdout.write(f"PT 등록 완료: {member1.name} - {program1.name}")
        
        # 8. 예약 생성
        reservation1, created = Reservation.objects.get_or_create(
            member=member1,
            trainer=trainer1,
            date=date.today(),
            start_time=time(14, 0),
            defaults={
                'pt_registration': registration1,
                'end_time': time(14, 30),
                'duration': 30,
                'reservation_status': 'confirmed'
            }
        )
        
        self.stdout.write(f"예약 생성 완료: {member1.name} - {trainer1.name}")
        
        # 9. 급여 데이터 생성
        salary1, created = Salary.objects.get_or_create(
            trainer=trainer1,
            year=2024,
            month=7,
            defaults={
                'base_salary': 3000000,
                'incentive_amount': 150000,
                'additional_revenue': 50000,
                'other_costs': 100000,
                'payment_status': 'paid'
            }
        )
        
        self.stdout.write(f"급여 데이터 생성 완료: {trainer1.name} - 2024년 7월")
        
        # 10. 지점 매출 데이터 생성
        revenue1, created = BranchRevenue.objects.get_or_create(
            branch=branch1,
            year=2024,
            month=7,
            defaults={
                'pt_revenue': 2000000,
                'membership_revenue': 500000,
                'additional_revenue': 300000
            }
        )
        
        self.stdout.write(f"지점 매출 데이터 생성 완료: {branch1.name} - 2024년 7월")
        
        # 11. 알림 템플릿 생성
        template1, created = NotificationTemplate.objects.get_or_create(
            name="예약 요청 알림",
            defaults={
                'notification_type': 'reservation_request',
                'title_template': "[Clamood] 새로운 PT 예약 요청",
                'message_template': "회원 {member_name}님이 {trainer_name} 트레이너에게 PT 예약을 요청했습니다."
            }
        )
        
        self.stdout.write("알림 템플릿 생성 완료")
        
        self.stdout.write("\n=== 샘플 데이터 생성 완료 ===")
        self.stdout.write(f"지점: {Branch.objects.count()}개")
        self.stdout.write(f"트레이너: {Trainer.objects.count()}개")
        self.stdout.write(f"회원: {Member.objects.count()}개")
        self.stdout.write(f"PT 프로그램: {PTProgram.objects.count()}개")
        self.stdout.write(f"PT 등록: {MemberPTRegistration.objects.count()}개")
        self.stdout.write(f"예약: {Reservation.objects.count()}개")
        self.stdout.write(f"급여: {Salary.objects.count()}개")
        self.stdout.write(f"지점 매출: {BranchRevenue.objects.count()}개") 