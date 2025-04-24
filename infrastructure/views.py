from django.db.migrations import serializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Asset, MaintenanceReport, RepairHistory, Located, SensorData
from .serializers import (
    RoomSerializer, AssetSerializer, MaintenanceReportSerializer, RepairHistorySerializer, RoomSerializer,
    SensorDataSerializer
)

class BaseDetailAPIView(APIView):
    model = None
    serializer_class = None

    def get(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)

    def put(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


class RoomDetailAPIView(BaseDetailAPIView):
    model = Located
    serializer_class = RoomSerializer

class AssetDetailAPIView(BaseDetailAPIView):
    model = Asset
    serializer_class = AssetSerializer

class MaintenanceReportDetailAPIView(BaseDetailAPIView):
    model = MaintenanceReport
    serializer_class = MaintenanceReportSerializer

class RepairHistoryDetailAPIView(BaseDetailAPIView):
    model = RepairHistory
    serializer_class = RepairHistorySerializer

class BaseListCreateAPIView(APIView):
    model = None
    serializer_class = None

    def get(self, request):
        instances = self.model.objects.all()
        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomListCreateAPIView(BaseListCreateAPIView):
    model = Located
    serializer_class = RoomSerializer

class AssetListCreateAPIView(BaseListCreateAPIView):
    model = Asset
    serializer_class = AssetSerializer

class MaintenanceReportListCreateAPIView(BaseListCreateAPIView):
    model = MaintenanceReport
    serializer_class = MaintenanceReportSerializer

class RepairHistoryListCreateAPIView(BaseListCreateAPIView):
    model = RepairHistory
    serializer_class = RepairHistorySerializer

class InfrastructureDataAPIView(APIView):
    def get(self, request):
        documents = self.collect_all_data()
        return Response({'documents': documents}, status=status.HTTP_200_OK)

    @staticmethod
    def collect_all_data():
        documents = []

        try:
            rooms = Located.objects.all()
            for room in rooms:
                serializer = RoomSerializer(room)
                documents.append(str(serializer.data))
        except Exception as e:
            print(f"Room 데이터 오류: {e}")

        try:
            assets = Asset.objects.all()
            for asset in assets:
                serializer = AssetSerializer(asset)
                documents.append(str(serializer.data))
        except Exception as e:
            print(f"Asset 데이터 오류: {e}")

        try:
            reports = MaintenanceReport.objects.all()
            for report in reports:
                serializer = MaintenanceReportSerializer(report)
                documents.append(str(serializer.data))
        except Exception as e:
            print(f"Report 데이터 오류: {e}")

        try:
            histories = RepairHistory.objects.all()
            for history in histories:
                serializer = RepairHistorySerializer(history)
                documents.append(str(serializer.data))
        except Exception as e:
            print(f"History 데이터 오류: {e}")

        try:
            sensors = SensorData.objects.all()
            for sensor in sensors:
                serializer = SensorDataSerializer(sensor)
                documents.append(str(serializer.data))
        except Exception as e:
            print(f"Sensor 데이터 오류: {e}")

        if not documents:
            return ["No data available."]

        return documents

class SensorDataListAPIView(BaseListCreateAPIView):
    model = SensorData
    serializer_class = SensorDataSerializer