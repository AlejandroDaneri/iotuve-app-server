import datetime
from src.schemas.comment import CommentSchema
from src.schemas.video import VideoSchema
from src.models.comment import Comment
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


def get_video(video_id):
    return Video.objects(id=video_id).first()


def get_comment(comment_id):
    return Comment.objects(id=comment_id).first()


def delete_all():
    Comment.objects().delete()
    Video.objects().delete()

