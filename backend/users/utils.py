import re


def name_is_valid(value):
    return re.compile(r'^[\w.@+-]+$').match(value) is not None
