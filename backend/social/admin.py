# backend/social/admin.py
from django.contrib import admin
from .models import Post, Comment, Follow, Story

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'text_preview', 'media_type', 'like_count', 'expires_at', 'is_expired']
    list_filter = ['media_type', 'created_at', 'expires_at']
    search_fields = ['text', 'user__username']
    readonly_fields = ['size_bytes', 'created_at', 'expires_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'text_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text', 'user__username']
    
    def text_preview(self, obj):
        return obj.text[:50] + "..."
    text_preview.short_description = 'Comment'

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'text', 'expires_at', 'is_expired']
    list_filter = ['expires_at', 'created_at']
