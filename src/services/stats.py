from bson.son import SON
from src.models.comment import Comment
from src.models.friendship import Friendship
from src.models.stat import Stat
from src.models.video import Video
from src.models.reaction import Like, Dislike, View


class StatisticsService:

    @staticmethod
    def count_requests(date_from, date_to):
        return Stat.objects(timestamp__gte=date_from, timestamp__lte=date_to).count()

    @staticmethod
    def rpm(date_from, date_to):
        pipeline = [
            {'$project': {
                'datetime': {
                    '$dateToString': {
                        'date': '$timestamp',
                        'format': '%Y-%m-%d %H:%M'
                    }}}},
            {"$group": {
                "_id": '$datetime',
                "count": {
                    "$sum": 1
                }
            }}
        ]
        return (req for req in Stat.objects(
            timestamp__gte=date_from, timestamp__lte=date_to).aggregate(pipeline))

    @staticmethod
    def count_requests_grouped_by_status(date_from, date_to):
        pipeline = [
            {"$group": {
                "_id": {
                    "status": "$status"
                },
                "count": {
                    "$sum": 1
                }
            }}
        ]
        result = {}
        for req in Stat.objects(timestamp__gte=date_from, timestamp__lte=date_to).aggregate(pipeline):
            result[str(req["_id"]["status"])] = req["count"]
        return result

    @staticmethod
    def count_requests_grouped_by_path(date_from, date_to):
        pipeline = [
            {"$group": {
                "_id": {
                    "path": "$path"
                },
                "count": {
                    "$sum": 1
                }
            }},
            {"$sort": SON([("count", -1), ("_id", -1)])}
        ]
        result = {}
        for req in Stat.objects(timestamp__gte=date_from, timestamp__lte=date_to).aggregate(pipeline):
            result[str(req["_id"]["path"])] = req["count"]
        return result

    @staticmethod
    def count_videos(date_from, date_to):
        return Video.objects(date_created__gte=date_from, date_created__lte=date_to).count()

    @staticmethod
    def count_comments(date_from, date_to):
        return Comment.objects(date_created__gte=date_from, date_created__lte=date_to).count()

    @staticmethod
    def count_friendships(date_from, date_to):
        return Friendship.objects(date_created__gte=date_from, date_created__lte=date_to).count()

    @staticmethod
    def top_likes():
        return Video.objects().order_by('-count_likes').limit(10).fields(title=1, count_likes=1)

    @staticmethod
    def top_dislikes():
        return Video.objects().order_by('-count_dislikes').limit(10).fields(title=1, count_dislikes=1)

    @staticmethod
    def top_most_viewed_videos():
        return Video.objects().order_by('-count_views').limit(10).fields(title=1, count_views=1)

    @staticmethod
    def count_approved_friendships():
        return Friendship.objects(status__exact="approved").count()

    @staticmethod
    def count_pending_friendships():
        return Friendship.objects(status__exact="pending").count()

    # @staticmethod
    # TODO: falta Model View
    # def top_active_users():
    #     pipeline = [
    #         {"$group": {"_id": "$user", "count": {"$sum": 1}}},
    #         {{"$sort": {"count": -1}}},
    #         {"$limit": 10}
    #     ]
    #     result = {}
    #     for req in View.objects().aggregate(pipeline):
    #         result[str(req["_id"]["user"])] = req["count"]
    #     return result


    # TypeError: string indices must be integers
    @staticmethod
    def min_max_avg_comments():
        pipeline = [
            {"$project": {
                "user": 1,
                "content": 1,
                "content_len": {"$strLenCP": "$content"}
            }},
            {"$group": {
                "_id": "null",  # TODO: revisar si es con null
                "max": {"$max": "$content_len"},
                "min": {"$min": "$content_len"},
                "avg": {"$avg": "$content_len"}
            }}

        ]
        result = {}
        # TODO: deberia ser solo uno
        for req in Comment.objects().aggregate(pipeline):
            result[str(req["_id"]["video"])] = [req["min"], req["max"], req["avg"]]
        return result

    # result[str(req["_id"]["user"])] = req["count"]
    # TypeError: string indices must be integers

    @staticmethod
    def top_writer_users():
        pipeline = [
            {"$group": {"_id": "$user", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        result = {}
        for req in Comment.objects().aggregate(pipeline):
            result[str(req["_id"]["user"])] = req["count"]
        return result

    # seguro tira el mismo error que el de arriba
    @staticmethod
    def count_visibility():
        pipeline = [
            {"$group": {"_id": "$visibility", "count": {"$sum": 1}}},
        ]
        return [doc for doc in Comment.objects().aggregate(pipeline)]

    # TODO: falta Model Like
    @staticmethod
    def top_liker():
        pipeline = [
            {"$group": {"_id": "$user", "count": {"$sum": 1}}},
            {{"$sort": {"count": -1}}},
            {"$limit": 10}
        ]
        result = {}
        for req in Like.objects().aggregate(pipeline):
            result[str(req["_id"]["visibility"])] = req["count"]
        return result

    # TODO: falta Model Dislike
    @staticmethod
    def top_disliker():
        pipeline = [
            {"$group": {"_id": "$user", "count": {"$sum": 1}}},
            {{"$sort": {"count": -1}}},
            {"$limit": 10}
        ]
        result = {}
        for req in Dislike.objects().aggregate(pipeline):
            result[str(req["_id"]["visibility"])] = req["count"]
        return result




