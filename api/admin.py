from django.contrib import admin
from openai import models
from api.models import *

# Register your models here.
@admin.register(DocumentEmbedding)
class DocumentEmbeddingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_preview', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('embedding', 'created_at')
    ordering = ('-created_at',)

    def name_preview(self, obj):
        return obj.name[:50]
    name_preview.short_description = "텍스트 미리보기"


@admin.register(RequestChatGPT)
class RequestChatGPTAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_preview', 'created_at')
    search_fields = ('text', 'response')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def text_preview(self, obj):
        return obj.text[:50]
    text_preview.short_description = "요청 미리보기"