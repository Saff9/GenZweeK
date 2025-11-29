# backend/social/views.py
from django.db.models import F
from django.utils import timezone
from rest_framework import viewsets, permissions, decorators, response, status
from rest_framework.decorators import action
from .models import Post, Comment, Follow, Story
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, StorySerializer
from .utils import compute_post_score

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Post.objects.filter(
            is_deleted=False, 
            expires_at__gte=timezone.now()
        ).select_related('user').order_by('-created_at')
        return qs

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        liked = request.data.get('liked', True)
        if liked:
            post.like_count = F('like_count') + 1
        else:
            post.like_count = F('like_count') - 1
        post.save(update_fields=['like_count'])
        post.refresh_from_db()
        return response.Response({'like_count': post.like_count})

    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        post = self.get_object()
        post.view_count = F('view_count') + 1
        post.save(update_fields=['view_count'])
        post.refresh_from_db()
        return response.Response({'view_count': post.view_count})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('post', 'user').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.select_related('follower', 'following').all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(expires_at__gte=timezone.now())
