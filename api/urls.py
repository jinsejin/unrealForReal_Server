from django.urls import path, include
from . import views

urlpatterns = [
    # path('save-embedding/', views.SaveEmbeddingAPIView.as_view(), name='save_embedding'),
    path('chat-with-rag/',views.ChatWithRagAPIView.as_view(), name='save_infrastructure_data'),
    path('save-infrastructure-data/', views.SaveInfrastructureDataAPIView.as_view(), name='chat_with_rag'),
]   