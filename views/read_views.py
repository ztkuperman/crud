import flask
from flask import session,abort
from infrastructure.view_modifiers import response
import services.auth_service as auth_svc
import services.post_service as post_svc
import services.user_service as user_svc

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
    if not auth_svc.authorize_post(session['username'], post):
        abort(403)
    return {'post' : post, "csrf_token":user_svc.csrf_new_token()}

@blueprint.route('/drafts')
@response(template_file='read/drafts.html')
def drafts():
    posts = post_svc.get_posts(status='draft')
    return {'posts':posts}

@blueprint.route('/myposts')
@response(template_file='read/myposts.html')
def myposts():
    posts = post_svc.get_posts(author=session['username'])
    return {'posts':posts}
