import os

# Tests run with DEBUG on so SECRET_KEY can fall back to the dev key; CI may still set its own.
os.environ.setdefault("DEBUG", "true")
