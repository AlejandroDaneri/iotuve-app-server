from src.resources.status import Home, Ping, TestDB, Stats
from src.resources.sessions import Sessions
from src.resources.users import Users, UsersList, Recovery


def init_routes(api):
    api.add_resource(Home, "/")
    api.add_resource(Ping, "/ping")
    api.add_resource(TestDB, "/testdb")
    api.add_resource(Stats, "/stats")

    api.add_resource(Sessions, "/sessions")

    api.add_resource(Users, "/users/<string:username>")
    api.add_resource(UsersList, "/users")

    api.add_resource(Recovery, "/recovery/<string:username>")
