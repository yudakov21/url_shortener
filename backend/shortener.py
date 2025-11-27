import string
from secrets import choice


ALPHABET: str = string.ascii_letters + string.digits


def generate_random_slug():
    return "".join(choice(ALPHABET) for _ in range(6))
