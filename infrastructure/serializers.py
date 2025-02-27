from rest_framework import serializers
from .models import Campus, Building, Floor, Room, Asset, MaintenanceReport, RepairHistory

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class MaintenanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceReport
        fields = '__all__'

class RepairHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairHistory
        fields = '__all__'


# ✅ 1. Serializer의 주요 역할
# 1️⃣ 직렬화 (Serialization)
#Django 모델 데이터를 JSON 형식으로 변환하여 API 응답으로 보낼 수 있도록 함.
#serializer.data를 호출하면 모델 데이터가 JSON으로 변환됨.
# 2️⃣ 역직렬화 (Deserialization)
#클라이언트에서 받은 JSON 데이터를 Django 모델 인스턴스로 변환하여 데이터베이스에 저장 가능.
#serializer.save()를 호출하면 create() 또는 update()가 실행됨.
# 3️⃣ 데이터 검증 (Validation)
# API 요청이 들어올 때, 데이터가 올바른지 검사하고 자동으로 에러를 반환할 수 있음.
# is_valid()를 호출하면 필수 필드 확인 및 유효성 검사를 수행함.