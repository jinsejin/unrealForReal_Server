# api/serializers.py
from rest_framework import serializers
from .models import DocumentEmbedding, RequestChatGPT

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
        fields = ['id', 'name', 'embedding', 'created_at']  

class RequestChatGPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestChatGPT
        fields = '__all__'