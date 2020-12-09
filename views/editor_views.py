import flask
from flask import request

from infrastructure.view_modifiers import response
import services.post_service as post_svc
import services.user_service as user_svc
blueprint = flask.Blueprint('editor', __name__, template_folder='templates')


@blueprint.route('/tinymce', methods = ['GET'])
@response(template_file='editor/tinymce.html')
def tinymce():
    post_id = int(request.args.get('post_id'))
    if post_id == 0:
        return {"post_id":post_id,
                "csrf_token": user_svc.csrf_new_token(),
                }
    elif post_id != 0:
        post = post_svc.get_single_post(post_id)
        print(post,post.__dict__)
        return {"post_id":post_id,
                "title":post.title,
                "content":post.content,
                "csrf_token": user_svc.csrf_new_token(),
                }


# Currently unused, this is an alternative editor to TinyMCE
#@blueprint.route('/trix')
#@response(template_file='editor/trix.html')
#def trix():
#    return {"":""}
