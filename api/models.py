from django.db import models
from django.contrib.postgres.fields import JSONField  # SQLite에서도 사용 가능
from sentence_transformers import SentenceTransformer


# 벡터 변환 모델
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class DocumentEmbedding(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()  # 원본 텍스트
    embedding = models.JSONField()  # JSON 필드를 이용해 벡터 저장 (SQLite 호환)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name[:50]  # 일부 텍스트 미리보기


class RequestChatGPT(models.Model):
    text = models.TextField()  # 사용자 입력 텍스트
    response = models.TextField()  # GPT-3 응답
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]  # 일부 텍스트 미리보기