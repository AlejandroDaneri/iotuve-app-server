from mongoengine.queryset.visitor import Q
from src.conf.database import db
from src.misc.importance import ImportanceCalculator


class Video(db.Document):
    meta = {'strict': False}
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

    @staticmethod
    def update_videos_importance():
        for video in Video.objects():
            video.save()

    def save(self, *args, **kwargs):
        self.__set_importance()
        return super(Video, self).save(*args, **kwargs)

    def __set_importance(self):
        import datetime
        from .comment import Comment
        from .reaction import Like, Dislike, View
        from .friendship import Friendship
        video = {
            'user_posts': Video.objects(user=self.user).count(),
            'user_reactions': (Like.count_by_user(self.user) +
                               Dislike.count_by_user(self.user) +
                               View.count_by_user(self.user)),
            'user_friends': Friendship.count_user_friends(self.user),
            'days': (self.date_created.date() - datetime.date.today()).days,
            'likes': self.count_likes,
            'dislikes': self.count_dislikes,
            'views': self.count_views,
            'comments': Comment.count_by_video(self.id) if self.id else 0,
            'importance': 0
        }

        self.importance = ImportanceCalculator(video).calculate_importance()
