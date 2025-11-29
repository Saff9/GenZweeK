# backend/social/serializers.py
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Post, Comment, Follow, Story

class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "user_id", "text", "media_type", "media_file", "size_bytes",
            "like_count", "comment_count", "view_count", "created_at",
            "expires_at", "is_expired"
        ]
        read_only_fields = [
            "size_bytes", "like_count", "comment_count", "view_count",
            "created_at", "expires_at", "is_expired"
        ]

    def validate(self, attrs):
        text = attrs.get("text", "").strip()
        if not text:
            raise serializers.ValidationError("Text content is required.")
        if len(text) > 2000:
            raise serializers.ValidationError("Text is too long (max 2000 chars).")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "user_id", "text", "created_at"]
        read_only_fields = ["user_id", "created_at"]

    def validate(self, attrs):
        text = attrs.get("text", "").strip()
        if not text:
            raise serializers.ValidationError("Comment text is required.")
        if len(text) > 500:
            raise serializers.ValidationError("Comment too long (max 500 chars).")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)

class FollowSerializer(serializers.ModelSerializer):
    following_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Follow
        fields = ["id", "following_id", "created_at"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["follower"] = user
        validated_data["following_id"] = validated_data.pop("following_id")
        return super().create(validated_data)

class StorySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Story
        fields = ["id", "user_id", "text", "media_file", "created_at", "expires_at"]
        read_only_fields = ["user_id", "created_at", "expires_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)
