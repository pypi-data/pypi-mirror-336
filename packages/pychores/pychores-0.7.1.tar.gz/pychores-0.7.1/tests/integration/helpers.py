import json

from pychores.model import User


def object_match_dict(obj, dictionary, whitelist=[]):
    for k, v in dictionary.items():
        if getattr(obj, k) != v and k not in whitelist:
            return False
    return True


def get_auth_headers(user: User) -> dict[str, str]:
    token = {
        "preferred_username": user.username,
        "email": user.email,
    }
    return {"Authorization": f"Bearer {json.dumps(token)}"}
