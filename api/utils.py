import os

from auth0.v3.authentication import Users


DOMAIN = os.getenv("DOMAIN")
assert DOMAIN is not None, "Domain Not Found"


def get_user_info(token: str):
    users = Users(DOMAIN)
    user = users.userinfo(token)
    sub = user.get("sub")
    if sub is None:
        raise Exception("Not Found User Id")
    user_id = sub.split("|")[-1]
    return user_id
