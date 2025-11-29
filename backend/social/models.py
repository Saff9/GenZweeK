# backend/social/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

USER_MODEL = settings.AUTH_USER_MODEL

class Post(models.Model):
    MEDIA_NONE = "none"
    MEDIA_IMAGE = "image"
    MEDIA_VIDEO = "video"
    MEDIA_TYPE_CHOICES = [
        (MEDIA_NONE, "None"),
        (MEDIA_IMAGE, "Image"),
        (MEDIA_VIDEO, "Video"),
    ]

    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField()
    media_type = models.CharField(
        max_length=10, choices=MEDIA_TYPE_CHOICES, default=MEDIA_NONE
    )
    media_file = models.FileField(upload_to="posts/media/", blank=True, null=True)
    size_bytes = models.BigIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.media_file:
            self.size_bytes = self.media_file.size
            if self.media_type == self.MEDIA_IMAGE and self.size_bytes > 10 * 1024 * 1024:
                raise ValueError("Image file too large (max 10 MB).")
            if self.media_type == self.MEDIA_VIDEO and self.size_bytes > 50 * 1024 * 1024:
                raise ValueError("Video file too large (max 50 MB).")
        else:
            self.media_type = self.MEDIA_NONE
            self.size_bytes = 0

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at or self.is_deleted

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

class Follow(models.Model):
    follower = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

class Story(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="stories")
    text = models.CharField(max_length=280, blank=True)
    media_file = models.FileField(upload_to="stories/media/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at
