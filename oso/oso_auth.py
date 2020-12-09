from oso import Oso
from flask import session

oso = Oso()

def init_oso():
    import data.__all_models as am
    global oso

    oso.register_class(am.crud.data.post.Post)
    oso.register_class(am.crud.data.users.User)
    oso.load_file('oso/route_access.polar')
    oso.load_file('oso/post_access.polar')
    return oso
