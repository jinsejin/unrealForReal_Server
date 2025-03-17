# api/serializers.py
from rest_framework import serializers
from .models import DocumentEmbedding

class DocumentEmbeddingSerializer(serializers.ModelSerializer):
    embedding = serializers.ListField(child=serializers.FloatField())
    # parsed_text = serializers.SerializerMethodField(read_only=True)

    def get_parsed_text(self, obj):
        import json
        try:
            return json.loads(obj.text)  # "{'id': 1, 'name': 'handong university'}" -> 딕셔너리
        except json.JSONDecodeError:
            return obj.text
        
    class Meta:
        model = DocumentEmbedding
        fields = ['id', 'text', 'embedding', 'created_at']  

class RequestChatGPTSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)
    user_id = serializers.CharField(max_length=100, required=False)  # 사용자 식별 (선택)
    request_type = serializers.ChoiceField(
        choices=[('RAG', 'RAG 요청'), ('GENERAL', '일반 요청')],
        default='RAG'
    )  # 요청 타입 구분

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("텍스트는 비어 있을 수 없습니다.")
        return value

    def create(self, validated_data):
        # 모델이 없으므로 단순히 데이터 반환
        return validated_data