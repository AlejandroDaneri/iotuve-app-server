import datetime
from http import HTTPStatus
from flask import make_response, request, g
from flask import current_app as app
from flask_restful import Resource
from marshmallow import ValidationError
from src.misc.authorization import check_token
from src.misc.responses import response_error
from src.models.comment import Comment
from src.models.video import Video
from src.schemas.comment import CommentSchema, CommentPaginatedSchema


class Comments(Resource):
    @check_token
    def get(self, comment_id):
        schema = CommentSchema()
        comment = Comment.objects(id=comment_id).first_or_404()
        return make_response(schema.dump(comment), HTTPStatus.OK)


class CommentsList(Resource):
    @check_token
    def get(self):
        schema = CommentPaginatedSchema()
        paginated = schema.load(request.args)
        comment = Comment.objects(**paginated["filters"]).skip(paginated["offset"]).limit(paginated["limit"])
        return make_response(dict(data=schema.dump(comment, many=True)), HTTPStatus.OK)

    @check_token
    def post(self):
        schema = CommentSchema()
        try:
            comment = schema.load(request.get_json(force=True))
        except ValidationError as e:
            return response_error(HTTPStatus.BAD_REQUEST, str(e.normalized_messages()))
        Video.objects(id=comment.video).first_or_404()
        if comment.parent:
            Comment.objects(id=comment.parent, video=comment.video).first_or_404()
        now = datetime.datetime.utcnow()
        comment.user = g.session_username
        comment.date_created = now
        comment.date_updated = now
        comment.save()
        return make_response(schema.dump(comment), HTTPStatus.CREATED)
