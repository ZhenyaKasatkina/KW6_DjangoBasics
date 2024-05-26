import secrets
import string


def make_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for item in range(10))
