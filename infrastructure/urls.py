from django.urls import path, include
from infrastructure.views import (
    RoomListCreateAPIView, RoomDetailAPIView,
    AssetListCreateAPIView, AssetDetailAPIView, MaintenanceReportListCreateAPIView, MaintenanceReportDetailAPIView,
    RepairHistoryListCreateAPIView, RepairHistoryDetailAPIView, InfrastructureDataAPIView , SensorDataListAPIView
)

urlpatterns = [
    path('api/sensor/', SensorDataListAPIView.as_view(), name='sensor-data-list'),
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