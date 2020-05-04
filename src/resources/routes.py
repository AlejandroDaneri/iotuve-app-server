from .status import Home, Ping, TestDB


def initialize_routes(api, api_path):
    api.add_resource(Home, "/")
    api.add_resource(Ping, api_path + "/ping")
    api.add_resource(TestDB, api_path + "/testdb")
