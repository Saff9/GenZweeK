# backend/social/utils.py
import math
from django.utils import timezone
from .models import Post

def compute_post_score(post: Post) -> float:
    """
    GenZweeK feed algorithm - text-first ranking:
    - 1.5x recency decay (fresh content first)
    - 0.5x comments (conversation priority)
    - 0.3x likes (engagement)
    - 0.1x views (logarithmic to prevent spam)
    - 1.1x boost for pure text posts
    """
    now = timezone.now()
    age_hours = max((now - post.created_at).total_seconds() / 3600.0, 0.1)
    time_decay = 1.0 / (age_hours + 1.0)

    likes = post.like_count
    comments = post.comment_count
    views = post.view_count

    score = (
        1.5 * time_decay +
        0.5 * comments +
        0.3 * likes +
        0.1 * math.log(views + 1)
    )
    
    # Text-first boost
    if post.media_type == Post.MEDIA_NONE:
        score *= 1.1
    
    return score

def cleanup_expired_content():
    """Management command helper - delete expired posts/stories"""
    from django.utils import timezone
    now = timezone.now()
    
    deleted_posts = Post.objects.filter(
        expires_at__lt=now, is_deleted=False
    ).update(is_deleted=True)
    
    deleted_stories = Story.objects.filter(
        expires_at__lt=now
    ).delete()
    
    return deleted_posts, deleted_stories
