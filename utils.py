import hashlib
import platform
from flask import session

def is_logged():
    username = session.get("username")
    if username is None:
        return False
    return True
