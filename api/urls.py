from django.urls import path, include
from . import views

urlpatterns = [
    path('chat_rag/',views.ChatWithRagAPIView.as_view(), name='save_infrastructure_data'),
    path('save_data/', views.SaveInfrastructureDataAPIView.as_view(), name='chat_with_rag'),
]   