import datetime
import uuid
from src.schemas.comment import CommentSchema
from src.schemas.friendship import FriendshipSchema
from src.schemas.stat import StatSchema
from src.schemas.video import VideoSchema
from src.models.comment import Comment
from src.models.friendship import Friendship
from src.models.like import Like
from src.models.stat import Stat
from src.models.video import Video


def save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:36:53.074000', status=200, time=0.000438690185546875):
    data_json = {'path': path, 'full_path': path,
                 'headers': {'Host': 'localhost', 'User-Agent': 'werkzeug/1.0.1'},
                 'host': 'localhost', 'method': 'GET', 'remote_ip': '127.0.0.1',
                 'request_id': '67910060-3a28-46a3-9957-f037f6661e28', 'status': status, 'time': time,
                 'timestamp': timestamp, 'version': 'v1'}
    schema = StatSchema()
    new_stat = schema.load(data_json)
    new_stat.save()


def save_new_video(date_created=None):
    post_json = {
        'title': 'Un titulo',
        'description': 'Una descripcion',
        'visibility': 'public',
        'media': {
            'name': 'mediafile',
            'date_created': '2020-05-30T02:36:53.074000',
            'size': 3215421,
            'type': 'video/mp4'
        },
        'location': {
            'latitude': 1212121.232323,
            'longitude': 1212121.232323
        }
    }
    schema = VideoSchema()
    new_video = schema.load(post_json)
    now = datetime.datetime.utcnow() if not date_created else date_created
    new_video.user = 'testuser'
    new_video.date_created = now
    new_video.date_updated = now
    new_video.save()
    return new_video


def save_new_comment(video=None, parent=None, date_created=None):
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
    now = datetime.datetime.utcnow() if not date_created else date_created
    new_comment.user = "testuser"
    new_comment.date_created = now
    new_comment.date_updated = now
    new_comment.save()
    return new_comment


def save_new_video_like(video=None, user=None, date_created=None):
    if not video:
        video = save_new_video().id
    new_like = Like()
    now = datetime.datetime.utcnow() if not date_created else date_created
    new_like.video = str(video)
    new_like.user = "testuser" if not user else user
    new_like.date_created = now
    new_like.save()
    video = Video.objects(id=str(video)).first()
    video.count_likes += 1
    video.save()
    return new_like


def save_new_friendship(from_user=None, to_user=None, status="pending", date_created=None):
    from_user = from_user or "fromusertest_%s" % uuid.uuid4()
    to_user = to_user or "tousertest_%s" % uuid.uuid4()

    post_json = {
        "message": "Este es un mensaje de prueba",
        "to_user": to_user
    }

    schema = FriendshipSchema()
    new_friendship = schema.load(post_json)
    now = datetime.datetime.utcnow() if not date_created else date_created
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


def get_like(video_id, user_id):
    return Friendship.objects(video=video_id, user=user_id).first()


def delete_all():
    Comment.objects().delete()
    Friendship.objects().delete()
    Like.objects().delete()
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