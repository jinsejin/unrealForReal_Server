from django.db import models

# Create your models here.
# 책상의 상태(고장이 났는지), 책상의 아이디 (몇번 책상이 고장났는지)
# 학교 건물
class Campus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
# 건물
class Building(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name="buildings")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.campus.name} - {self.name}"
# 층
class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="floors")
    number = models.IntegerField()

    def __str__(self):
        return f"{self.building} - {self.number}층"

class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.floor.name} - {self.name}"


class Asset(models.Model):
    ASSET_CATEGORIES = [
        ('STRUCTURE', '구조물'),
        ('FACILITY', '설비'),
        ('FURNITURE', '가구'),
        ('ELECTRONIC', '전자기기'),
        ('OTHER', '기타'),
    ]

    STATE_CHOICES = [
        ('NORMAL', '정상'),
        ('BROKEN', '고장'),
        ('UNDER_REPAIR', '수리 중'),
        ('NEEDS_REPLACEMENT', '교체 필요'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="assets")  # 방과 연결
    category = models.CharField(max_length=20, choices=ASSET_CATEGORIES, default='OTHER')  # 분류
    name = models.CharField(max_length=100)  # 사물 이름
    install_date = models.DateField(null=True, blank=True)  # 설치 날짜
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='NORMAL')  # 현재 상태

    def __str__(self):
        return f"{self.room.floor.building.name} {self.room.floor.number}층 {self.room.name} - {self.name}"

#고장 신고
class MaintenanceReport(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', '긴급'),
        ('MEDIUM', '보통'),
        ('LOW', '낮음'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="reports")  # 고장 신고 대상
    user = models.CharField(max_length=100)  # 신고자 (학생, 교수, 관리자 등)
    description = models.TextField()  # 신고 내용
    reported_at = models.DateTimeField(auto_now_add=True)  # 신고 날짜
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')  # 우선순위
    is_resolved = models.BooleanField(default=False)  # 해결 여부

    def __str__(self):
        return f"{self.asset.name} - {self.priority} ({'해결됨' if self.is_resolved else '미해결'})"


#7. 수리 이력 (Repair History)
class RepairHistory(models.Model):
    report = models.OneToOneField(MaintenanceReport, on_delete=models.CASCADE, related_name="repair")  # 고장 신고와 연결
    repaired_by = models.CharField(max_length=100)  # 수리 담당자
    repair_details = models.TextField()  # 수리 내용
    repaired_at = models.DateTimeField(auto_now_add=True)  # 수리 완료 날짜

    def __str__(self):
        return f"{self.report.asset.name} - 수리 완료"

# class 건물
# class
# class 'A(미정)'의 속성 교유 ID , location, category, status , failure type