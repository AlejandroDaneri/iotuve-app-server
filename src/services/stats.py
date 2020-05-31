from bson.son import SON
from src.models.comment import Comment
from src.models.friendship import Friendship
from src.models.stat import Stat
from src.models.video import Video


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