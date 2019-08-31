from validate_email import validate_email


def non_empty_string(s):
    if not s:
        raise ValueError("This field cannot be empty.")
    return s


def email(email_str):
    """Return email_str if valid, raise an exception in other case."""
    if not validate_email(non_empty_string(email_str)):
        raise ValueError('{} is not a valid email'.format(email_str))
    return email_str.lower()
