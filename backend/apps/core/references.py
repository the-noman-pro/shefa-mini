import secrets

# No 0/O or 1/I, so a reference read aloud or copied by hand stays unambiguous.
_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def make_reference(prefix, length=10):
    body = "".join(secrets.choice(_ALPHABET) for _ in range(length))
    return f"{prefix}-{body}"
