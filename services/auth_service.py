#For OSO authorization
import services.user_service as user_svc
from crud.oso.oso_auth import oso



def authorize_route(username:str, action: str, route: str):
    user = user_svc.get_user_by_name(username)
    return oso.is_allowed(user, "GET", route)


def authorize_post(username: str, post):
    user = user_svc.get_user_by_name(username)
    return oso.is_allowed(user, "read", post)
