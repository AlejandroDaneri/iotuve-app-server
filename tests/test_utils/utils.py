import datetime
import uuid
from src.schemas.comment import CommentSchema
from src.schemas.friendship import FriendshipSchema
from src.schemas.video import VideoSchema
from src.models.comment import Comment
from src.models.friendship import Friendship
from src.models.stat import Stat
from src.models.video import Video


def save_new_video():
    post_json = {
        "title": "Un titulo",
        "description": "Una descripcion",
        "visibility": "public",
        "media": {
            "url": "https://una.url.io/mediafield"
        },
        "location": {
            "latitude": 1212121.232323,
            "longitude": 1212121.232323
        }
    }
    schema = VideoSchema()
    new_video = schema.load(post_json)
    now = datetime.datetime.utcnow()
    new_video.user = "testuser"
    new_video.date_created = now
    new_video.date_updated = now
    new_video.save()
    return new_video


def save_new_comment(video=None, parent=None):
    if not video:
        video = save_new_video().id
    post_json = {
        "content": "Este es un comentario de prueba",
        "video": str(video),
        "user": "testuser"
    }
    if parent:
        post_json["parent"] = str(parent)
    schema = CommentSchema()
    new_comment = schema.load(post_json)
    now = datetime.datetime.utcnow()
    new_comment.user = "testuser"
    new_comment.date_created = now
    new_comment.date_updated = now
    new_comment.save()
    return new_comment


def save_new_friendship(from_user=None, to_user=None, status="pending"):
    from_user = from_user or "fromusertest_%s" % uuid.uuid4()
    to_user = to_user or "tousertest_%s" % uuid.uuid4()

    post_json = {
        "message": "Este es un mensaje de prueba",
        "to_user": to_user
    }

    schema = FriendshipSchema()
    new_friendship = schema.load(post_json)
    now = datetime.datetime.utcnow()
    new_friendship.from_user = from_user
    new_friendship.status = status
    new_friendship.date_created = now
    new_friendship.date_updated = now
    new_friendship.save()
    return new_friendship


def get_video(video_id):
    return Video.objects(id=video_id).first()


def get_comment(comment_id):
    return Comment.objects(id=comment_id).first()


def get_friendship(friendship_id):
    return Friendship.objects(id=friendship_id).first()


def delete_all():
    Comment.objects().delete()
    Friendship.objects().delete()
    Stat.objects().delete()
    Video.objects().delete()


# def test_stats(app):
#     import random
#     for _ in range(0, 4):
#         app.get('/api/v1/ping')
#         app.get('/api/v1/')
#
#     for _ in range(0, 10):
#         video = save_new_video()
#         for _ in range(0, random.randint(0, 6)):
#             comm = save_new_comment(video.id)
#
#             for _ in range(0, random.randint(0, 9)):
#                 save_new_comment(video.id, comm.id)
#
#     from src.services.stats import StatisticsService
#
#     import pprint
#     pprint.pprint(StatisticsService.count_requests(datetime.datetime(year=2020, month=5, day=28), datetime.datetime.utcnow()))
#     pprint.pprint(list(StatisticsService.count_requests_grouped_by_status(datetime.datetime(year=2020, month=5, day=28), datetime.datetime.utcnow())))
#     pprint.pprint(list(StatisticsService.count_requests_grouped_by_path(datetime.datetime(year=2020, month=5, day=28), datetime.datetime.utcnow())))
#     pprint.pprint(StatisticsService.count_videos(datetime.datetime(year=2020, month=5, day=28), datetime.datetime.utcnow()))
#     pprint.pprint(StatisticsService.count_comments(datetime.datetime(year=2020, month=5, day=28), datetime.datetime.utcnow()))
#     pprint.pprint(StatisticsService.count_friendships(datetime.datetime(year=2020, month=5, day=28), datetime.datetime.utcnow()))
#
#
#
#     return
#
#     from bson.son import SON
#
#     pipeline = [
#              #{"$unwind": "$tags"},
#              {"$group": {
#                  "_id": {
#                      "method": "$method",
#                      "status": "$status",
#                      "path": "$path",
#                  },
#                  "count": {
#                      "$sum": 1
#                  }
#              }},
#              {"$sort": SON([("count", -1), ("_id", -1)])}
#             ]
#     import pprint
#     pprint.pprint(list(Stat.objects.aggregate(pipeline)))

# def example_join(self):
#     from src.models.comment import Comment
#     for _ in range(1, 2):
#         comment = save_new_comment()
#         comment.save()
#         for _ in range(1, 3):
#             save_new_comment(parent=comment.id)
#
#     curosr = Comment.objects.aggregate(
#         [
#             {
#                 "$lookup":
#                 {
#                     "from": "comment",
#                     "localField": "_id",
#                     "foreignField": "parent",
#                     "as": "friendsData"
#                 }
#             },
#             {
#                 "$unwind": "$friendsData"
#             },
#             {
#                 "$group":
#                 {
#                     "_id": "$_id",
#                     "friendsData": { "$push": "$friendsData" }
#                 }
#             },
#         ]
#     )
#     import pprint
#     print(Comment._get_collection_name())
#     pprint.pprint(list(curosr))