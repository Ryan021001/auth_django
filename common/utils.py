import string
from random import SystemRandom


def generate_otp(length: int = 6):
    otp = ""
    for _ in range(length):
        otp += str(SystemRandom().randint(0, 9))
    return otp


def _gen_random_string(size, chars):
    result = ''.join(SystemRandom().choice(chars) for _ in range(size))
    return result


def gen_strong_password():
    password = _gen_random_string(12, (_gen_random_string(4, string.ascii_letters)
                                       + _gen_random_string(4, string.digits)
                                       + _gen_random_string(4, "*&%$#@!")))
    return password
