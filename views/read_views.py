import flask
from infrastructure.view_modifiers import response
import services.post_service as post_svc
import services.auth_service as auth_svc
blueprint = flask.Blueprint('read', __name__, template_folder='templates')

@blueprint.route('/')
@response(template_file = 'read/index.html')
def index():
    posts = post_svc.get_posts(status='public')
    return {'posts': posts}

@blueprint.route('/read/<int:post_id>')
@response(template_file= 'read/read.html')
def read(post_id: int):
    post = post_svc.get_single_post(post_id)
    return {'post' : post, "csrf_token":auth_svc.csrf_new_token()}

@blueprint.route('/drafts')
@response(template_file='read/drafts.html')
def drafts():
    posts = post_svc.get_posts(status='draft')
    return {'posts':posts}
