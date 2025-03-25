from typing import TypedDict


class Config(TypedDict):
    mongo_db_connection_string: str
    db_name: str
    rabbitmq_url: str
    rabbitmq_queue: str
    jwt_secret: str
    jwt_algorithm: str
    password_scheme: str


class TestMessage(TypedDict):
    title: str
