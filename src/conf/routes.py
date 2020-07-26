from src.resources.adminusers import AdminUsers, AdminUsersList, AdminUsersSessions
from src.resources.comments import Comments, CommentsList
from src.resources.fcm_tokens import FCMTokens
from src.resources.friendships import Friendships, FriendshipsList, FriendsByUser
from src.resources.reactions import Likes, Dislikes, Views
from src.resources.recovery import Recovery, RecoveryList
from src.resources.status import Home, Ping, Status, StatsNew
from src.resources.sessions import Sessions, SessionsOwner
from src.resources.users import Users, UsersList, UsersSessions, UsersAvatars
from src.resources.videos import Videos, VideosList
from src.conf import APP_PREFIX


def init_routes(api):
    api.add_resource(Home, "/", APP_PREFIX + "/")
    api.add_resource(Ping, "/ping", APP_PREFIX + "/ping")

    api.add_resource(StatsNew, "/stats", APP_PREFIX + "/stats")
    
    api.add_resource(Status, "/status", APP_PREFIX + "/status")

    api.prefix = APP_PREFIX

    api.add_resource(Sessions, "/sessions/<string:session>")
    api.add_resource(SessionsOwner, "/sessions")

    api.add_resource(Users, "/users/<string:username>")
    api.add_resource(UsersList, "/users")
    api.add_resource(UsersSessions, "/users/<string:username>/sessions")
    api.add_resource(UsersAvatars, '/users/<string:username>/avatars')

    api.add_resource(FCMTokens, "/fcm")

    api.add_resource(AdminUsers, "/adminusers/<string:username>")
    api.add_resource(AdminUsersList, "/adminusers")
    api.add_resource(AdminUsersSessions, "/adminusers/<string:username>/sessions")

    api.add_resource(Recovery, "/recovery/<string:username>")
    api.add_resource(RecoveryList, "/recovery")

    api.add_resource(Videos, "/videos/<string:video_id>")
    api.add_resource(VideosList, "/videos")

    api.add_resource(Comments, "/comments/<string:comment_id>")
    api.add_resource(CommentsList, "/comments")

    api.add_resource(Friendships, "/friendships/<string:friendship_id>")
    api.add_resource(FriendshipsList, "/friendships")
    api.add_resource(FriendsByUser, "/users/<string:username>/friends")

    api.add_resource(Likes, "/videos/<string:video_id>/likes")
    api.add_resource(Dislikes, "/videos/<string:video_id>/dislikes")
    api.add_resource(Views, "/videos/<string:video_id>/views")
