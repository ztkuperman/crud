import flask
from flask import redirect, url_for, request, session
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

from infrastructure.view_modifiers import response
import services.post_service as post_svc
import services.auth_service as auth_svc
blueprint = flask.Blueprint('update', __name__, template_folder='templates')


@blueprint.route('/create', methods=['Get',])
@response(template_file='update/create.html')
def create():
    return redirect(url_for('editor.tinymce',post_id=0))

@blueprint.route('/create', methods=['post'])
def create_post():
    if auth_svc.csrf_validate(request.form.get('csrf_token')):
        title = request.form['title']
        content = request.form['editor']
        author = session.get('username')
        post_id = post_svc.create_post(title,content,author)
        return redirect(url_for('read.read',post_id=post_id))
    else:
        return redirect(url_for('editor.tinymce',post_id=0))


@blueprint.route('/update/<int:post_id>', methods=['GET'])
def update_get(post_id: int):
    return redirect(url_for('editor.tinymce', post_id=post_id))


@blueprint.route('/update/<int:post_id>', methods=['post'])
def update_post(post_id: int):
    if auth_svc.csrf_validate(request.form.get('csrf_token')):
        title = request.form['title']
        content = request.form['editor']
        post_svc.update_post(post_id,title,content)
        return redirect(url_for('read.read', post_id=post_id))
    else:
        return redirect(url_for('editor.tinymce', post_id=post_id))


@blueprint.route('/delete', methods=["POST"])
def delete():
    if auth_svc.csrf_validate(request.form.get('csrf_token')):
        post_svc.delete_post(request.form.get('post_id'))
    return redirect(url_for('read.index'))

@blueprint.route('/publish', methods=['POST'])
def publish():
    post_id = request.form.get('post_id')
    if auth_svc.csrf_validate(request.form.get('csrf_token')):
        post_svc.publish_post(post_id)
    return redirect(url_for('read.read', post_id=post_id))
