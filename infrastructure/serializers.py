from rest_framework import serializers
from .models import  Located, Asset, MaintenanceReport, RepairHistory , SensorData

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Located
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


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'
