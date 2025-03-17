from django.urls import path, include
from infrastructure.views import (
    CampusListCreateAPIView, CampusDetailAPIView, BuildingListCreateAPIView, BuildingDetailAPIView,
    FloorListCreateAPIView, FloorDetailAPIView, RoomListCreateAPIView, RoomDetailAPIView,
    AssetListCreateAPIView, AssetDetailAPIView, MaintenanceReportListCreateAPIView, MaintenanceReportDetailAPIView,
    RepairHistoryListCreateAPIView, RepairHistoryDetailAPIView, InfrastructureDataAPIView
)

urlpatterns = [
    path('api/campus/', CampusListCreateAPIView.as_view(), name='campus-list-create'),
    path('api/campus/<int:pk>/', CampusDetailAPIView.as_view(), name='campus-detail'),
    path('api/building/', BuildingListCreateAPIView.as_view(), name='building-list-create'),
    path('api/building/<int:pk>/', BuildingDetailAPIView.as_view(), name='building-detail'),
    path('api/floor/', FloorListCreateAPIView.as_view(), name='floor-list-create'),
    path('api/floor/<int:pk>/', FloorDetailAPIView.as_view(), name='floor-detail'),
    path('api/room/', RoomListCreateAPIView.as_view(), name='room-list-create'),
    path('api/room/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),
    path('api/asset/', AssetListCreateAPIView.as_view(), name='asset-list-create'),
    path('api/asset/<int:pk>/', AssetDetailAPIView.as_view(), name='asset-detail'),
    path('api/maintenance-report/', MaintenanceReportListCreateAPIView.as_view(), name='maintenance-report-list-create'),
    path('api/maintenance-report/<int:pk>/', MaintenanceReportDetailAPIView.as_view(), name='maintenance-report-detail'),
    path('api/repair-history/', RepairHistoryListCreateAPIView.as_view(), name='repair-history-list-create'),
    path('api/repair-history/<int:pk>/', RepairHistoryDetailAPIView.as_view(), name='repair-history-detail'),
    path('data/', InfrastructureDataAPIView.as_view(), name='infrastructure_data'),
]