from mongoengine.queryset.visitor import Q
from src.conf.database import db


class Friendship(db.Document):
    from_user = db.StringField(required=True)
    to_user = db.StringField(required=True)
    message = db.StringField(required=False)
    status = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)
    date_updated = db.ComplexDateTimeField(required=True)

    @staticmethod
    def get_user_friends(user):
        return Friendship.objects((Q(from_user=user) | Q(to_user=user)) & Q(status="approved"))

    @staticmethod
    def count_user_friends(user):
        return Friendship.objects((Q(from_user=user) | Q(to_user=user)) & Q(status="approved")).count()

    @staticmethod
    def get_user_friends_list(user):
        query = (Q(from_user=user) | Q(to_user=user)) & Q(status="approved")
        friends = Friendship.objects(query).fields(to_user=1, from_user=1)
        return [friend.to_user if friend.to_user != user else friend.from_user for friend in friends]

    @staticmethod
    def get_friendship(friendship_id):
        return Friendship.objects(id=friendship_id).first()

    @staticmethod
    def get_friendships(filters, offset, limit):
        return Friendship.objects(**filters).skip(offset).limit(limit)

    @staticmethod
    def friendship_exist(user1, user2, status=None):
        query = ((Q(from_user=user1) & Q(to_user=user2)) | (Q(from_user=user2) & Q(to_user=user1)))
        if status:
            query &= Q(status=status)
        return Friendship.objects(query).count() > 0
