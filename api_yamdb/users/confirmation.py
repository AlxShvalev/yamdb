import random
import string

from django.core.mail import send_mail


def code_generator(email):
    letters_and_digits = string.ascii_letters + string.digits
    code = ''.join(random.sample(letters_and_digits, 10))

    send_mail(
        'Добро пожаловать в Yatube!',
        code,
        email,
        [email],
        fail_silently=False
    )

    return code
