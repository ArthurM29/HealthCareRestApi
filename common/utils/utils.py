import uuid


def random_string(length):
    """Return parts of UUID"""
    return str(uuid.uuid4())[:length].replace('-', '')
