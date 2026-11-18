import os

# Tests run with DEBUG on so SECRET_KEY can fall back to the dev key; CI may still set its own.
os.environ.setdefault("DEBUG", "true")


def pytest_sessionfinish(session, exitstatus):
    # pytest exits with 5 when it collects no tests. Treat an empty suite as a pass until the first
    # test exists; delete this hook then, so a mistyped test file name fails loudly.
    if exitstatus == 5:
        session.exitstatus = 0
