#! coding: utf8
import uuid
from flask import session


def make_error(result, code, message):
    result['code'] = code
    result['message'] = message

    return result


def create_token():
    return uuid.uuid1().get_hex()


def get_uid_by_token(token):
    return session.get('user_of_token_' + token)