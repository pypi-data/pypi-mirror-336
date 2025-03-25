import os
API_KEY = os.getenv("ARCANNA_INPUT_API_KEY")
ARCANNA_HOST = os.getenv("ARCANNA_HOST", "")
ARCANNA_USER = "MCP" + "-" + (os.getenv("ARCANNA_USER") or "user")
TRANSPORT_MODE = os.getenv("TRANSPORT_MODE", "sse")


def validate_environment_variables():
    if API_KEY is None:
        raise Exception("Arcanna input API KEY not found.")

    if ARCANNA_HOST is None:
        raise Exception("Arcanna HOST not found.")

    if TRANSPORT_MODE not in ["stdio", "sse"]:
        raise Exception(f"TRANSPORT_MODE {TRANSPORT_MODE} not supported.")