from src.resources.recovery import Recovery, RecoveryList
from src.resources.status import Home, Ping, Stats, Status
from src.resources.sessions import Sessions
from src.resources.users import Users, UsersList
from src.conf import APP_PREFIX


def init_routes(api):
    api.add_resource(Home, "/", APP_PREFIX + "/")
    api.add_resource(Ping, "/ping", APP_PREFIX + "/ping")
    api.add_resource(Stats, "/stats", APP_PREFIX + "/stats")
    api.add_resource(Status, "/status", APP_PREFIX + "/status")

    api.prefix = APP_PREFIX

    api.add_resource(Sessions, "/sessions")

    api.add_resource(Users, "/users/<string:username>")
    api.add_resource(UsersList, "/users")

    api.add_resource(Recovery, "/recovery/<string:username>")
    api.add_resource(RecoveryList, "/recovery")
