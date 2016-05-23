#! coding: utf8
from redis import Redis

g_redis_operator = Redis()


def get_uid_by_token(token):
    uid = g_redis_operator.get(token)
    return uid if uid else None