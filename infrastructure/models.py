from django.db import models

class Located(models.Model):
    campus_name = models.CharField(max_length=100)
    building_name = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=100, null=True, blank=True)  # 3D 좌표

class Asset(models.Model):
    ASSET_CATEGORIES = [
        ('STRUCTURE', '구조물'),
        ('FACILITY', '설비'),
        ('FURNITURE', '가구'),
        ('ELECTRONIC', '전자기기'),
        ('OTHER', '기타')
    ]
    STATE_CHOICES = [
        ('NORMAL', '정상'),
        ('BROKEN', '고장'),
        ('UNDER_REPAIR', '수리 중'),
        ('NEEDS_REPLACEMENT', '교체 필요'),
    ]

    room = models.ForeignKey(Located, on_delete=models.CASCADE, related_name="assets")
    asset_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    category = models.CharField(max_length=20, choices=ASSET_CATEGORIES, default='OTHER')
    name = models.CharField(max_length=100)
    install_date = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='NORMAL')

    @property
    def building_name(self):
        return self.room.building_name

    @property
    def room_name(self):
        return self.room.room_name

    def __str__(self):
        return self.name

class MaintenanceReport(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', '긴급'),
        ('MEDIUM', '보통'),
        ('LOW', '낮음')
    ]

    FAILURE_TYPES = [
        ('STRUCTURAL', '구조적 손상'),
        ('ELECTRICAL', '전기 문제'),
        ('MECHANICAL', '기계적 문제'),
        ('OTHER', '기타')
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="reports")
    user = models.CharField(max_length=100)
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    failure_type = models.CharField(max_length=20, choices=FAILURE_TYPES, default='OTHER')
    is_resolved = models.BooleanField(default=False)

    @property
    def building_name(self):
        return self.asset.room.building_name

    def __str__(self):
        return f"{self.asset.name} - {self.priority}"


class RepairHistory(models.Model):
    report = models.OneToOneField(MaintenanceReport, on_delete=models.CASCADE, related_name="repair")
    repaired_by = models.CharField(max_length=100)
    repair_details = models.TextField()
    repaired_at = models.DateTimeField(auto_now_add=True)


class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    angle = models.FloatField()
    is_door_open = models.BooleanField(default=False)
    is_person_there = models.BooleanField(default=False)
    airconditioner = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SensorData at {self.timestamp}"