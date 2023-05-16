import os


class DevConfig:
    DB_PATH = 'warehouse.db'


class TestConfig:
    DB_PATH = os.path.dirname(os.path.abspath(__file__)) + \
        "/test-resources/web_test_warehouse.db"
