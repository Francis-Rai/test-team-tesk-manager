import secrets
import string
import faker

fake = faker.Faker()


def generate_register_data():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": generate_email(),
        "password": generate_password(),
    }

def generate_password(length=12):
    allowed_symbols = "!@#$%^&*()_+-[]{};':\"\\|,.<>/?"
    chars = string.ascii_letters + string.digits + allowed_symbols

    password = (
        secrets.choice(string.ascii_lowercase) +
        secrets.choice(string.ascii_uppercase) +
        secrets.choice(string.digits) +
        secrets.choice(allowed_symbols) +
        ''.join(secrets.choice(chars) for _ in range(length - 4))
    )
    return ''.join(secrets.SystemRandom().sample(password, len(password)))


def generate_email():
    return f"user_{secrets.token_hex(4)}@test.com"


def copy_dict(d: dict, keys_to_copy: list = None) -> dict:
    """
    Return a new dict containing only the specified keys from the original dict.
    Keys that do not exist in the original dict are ignored.
    """
    if not keys_to_copy:
        return d.copy()  # full copy
    return {k: d[k] for k in keys_to_copy if k in d}
