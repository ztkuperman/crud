import flask
from infrastructure.view_modifiers import response
import services.post_service as post_svc

blueprint = flask.Blueprint('read', __name__, template_folder='templates')

@blueprint.route('/')
@response(template_file = 'read/index.html')
def index():
    posts = post_svc.get_posts()
    return {'posts': posts}

@blueprint.route('/read/<int:post_id>')
@response(template_file= 'read/read.html')
def read(post_id: int):
    post = post_svc.get_single_post(post_id)
    return {'post' : post}
