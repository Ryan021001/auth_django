from django.core.mail import EmailMessage
from decouple import config
import string
from random import SystemRandom
from django.core.mail import send_mail
from django_rq import job

# import ssl

# ssl._create_default_https_context = ssl._create_unverified_context


def generate_otp(length: int = 6):
    otp = ""
    for _ in range(length):
        otp += str(SystemRandom().randint(0, 9))
    return otp


def _gen_random_string(size, chars):
    result = "".join(SystemRandom().choice(chars) for _ in range(size))
    return result


def gen_strong_password():
    password = _gen_random_string(
        12,
        (
            _gen_random_string(4, string.ascii_letters)
            + _gen_random_string(4, string.digits)
            + _gen_random_string(4, "*&%$#@!")
        ),
    )
    return password


@job
def send_custom_email(
    subject,
    message,
    recipient_list,
    from_email=config("MAIL_USER", cast=str),
):
    send_mail(subject, message, from_email, recipient_list)
