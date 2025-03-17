from django.db.migrations import serializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Campus, Building, Floor, Room, Asset, MaintenanceReport, RepairHistory
from .serializers import (
    CampusSerializer, BuildingSerializer, FloorSerializer,
    RoomSerializer, AssetSerializer, MaintenanceReportSerializer, RepairHistorySerializer
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


class CampusDetailAPIView(BaseDetailAPIView):
    model = Campus
    serializer_class = CampusSerializer

class BuildingDetailAPIView(BaseDetailAPIView):
    model = Building
    serializer_class = BuildingSerializer

class FloorDetailAPIView(BaseDetailAPIView):
    model = Floor
    serializer_class = FloorSerializer

class RoomDetailAPIView(BaseDetailAPIView):
    model = Room
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

class CampusListCreateAPIView(BaseListCreateAPIView):
    model = Campus
    serializer_class = CampusSerializer

class BuildingListCreateAPIView(BaseListCreateAPIView):
    model = Building
    serializer_class = BuildingSerializer

class FloorListCreateAPIView(BaseListCreateAPIView):
    model = Floor
    serializer_class = FloorSerializer

class RoomListCreateAPIView(BaseListCreateAPIView):
    model = Room
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

def collect_all_data():
    
    documents = []

    # Campus 데이터
    campuses = Campus.objects.all()
    for campus in campuses:
        serializer = CampusSerializer(campus)
        documents.append(str(serializer.data))  # JSON 데이터를 문자열로 변환

    # Building 데이터
    buildings = Building.objects.all()
    for building in buildings:
        serializer = BuildingSerializer(building)
        documents.append(str(serializer.data))

    # Floor 데이터
    floors = Floor.objects.all()
    for floor in floors:
        serializer = FloorSerializer(floor)
        documents.append(str(serializer.data))

    # Room 데이터
    rooms = Room.objects.all()
    for room in rooms:
        serializer = RoomSerializer(room)
        documents.append(str(serializer.data))

    # Asset 데이터
    assets = Asset.objects.all()
    for asset in assets:
        serializer = AssetSerializer(asset)
        documents.append(str(serializer.data))

    # MaintenanceReport 데이터
    reports = MaintenanceReport.objects.all()
    for report in reports:
        serializer = MaintenanceReportSerializer(report)
        documents.append(str(serializer.data))

    # RepairHistory 데이터
    histories = RepairHistory.objects.all()
    for history in histories:
        serializer = RepairHistorySerializer(history)
        documents.append(str(serializer.data))

    return documents if documents else ["No data available."]

class InfrastructureDataAPIView(APIView):
    def get(self, request):
        documents = collect_all_data()
        return Response({'documents': documents}, status=status.HTTP_200_OK)