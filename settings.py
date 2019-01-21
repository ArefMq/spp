import random

COMMENT_CHAR = '#'
VALID_VARIABLE_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890#@_'
GITHUB_URL = 'http://github.com/arefmq/spp'
COPYRIGH_YEAR = '2019-2020'


def generate_random_name():
    name = '%05x' % random.getrandbits(32)
    return name[:5]

