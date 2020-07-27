from mongoengine.queryset.visitor import Q
from src.conf.database import db


class Video(db.Document):
    title = db.StringField(required=False, default=None)
    description = db.StringField(required=False, default=None)
    visibility = db.StringField(required=True)
    location = db.DictField(required=False, default=None)
    count_likes = db.IntField(required=True, default=0)
    count_dislikes = db.IntField(required=True, default=0)
    count_views = db.IntField(required=True, default=0)
    user = db.StringField(required=True)
    importance = db.IntField(required=False, default=0)
    date_created = db.ComplexDateTimeField(required=True)
    date_updated = db.ComplexDateTimeField(required=True)

    @staticmethod
    def get_videos(filters, offset, limit):
        return Video.objects(**filters).skip(offset).limit(limit)

    @staticmethod
    def get_videos_wall(wall_user, friends_wall_user, video_id, user, visibility, offset, limit):
        query = (Q(user__in=friends_wall_user) | (Q(visibility="public") & (Q(user__ne=wall_user))))
        query |= Q(user=wall_user)
        if video_id:
            query &= Q(id=video_id)
        if user:
            query &= Q(user=user)
        if visibility:
            query &= Q(visibility=visibility)
        return Video.objects(query).order_by('-importance').skip(offset).limit(limit)
