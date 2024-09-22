import humanize

from django.db.models import Count, OuterRef, Exists
from django.db.models.functions import Coalesce

from .models import Post, Like

def serialize_posts(posts, user):

    has_liked_subquery = Like.objects.filter(
        user=user,
        post=OuterRef('pk')
    ).values('id')

    posts = posts.annotate(
        likes_count=Count('likes'),
        has_liked=Coalesce(Exists(has_liked_subquery), False)
    )

    return [
        {
            'id': post.id,
            'creator': post.creator.username,
            'content': post.content,
            'created_at': format_datetime(post.created_at),
            'likes_count': post.likes_count,
            'has_liked': post.has_liked,
        }
        for post in posts
    ]

def format_datetime(dt):
    return humanize.naturaltime(dt)