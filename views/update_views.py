import flask
from flask import redirect, url_for, request
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

from infrastructure.view_modifiers import response
import services.post_service as post_svc

blueprint = flask.Blueprint('update', __name__, template_folder='templates')


@blueprint.route('/create', methods=['Get',])
@response(template_file='update/create.html')
def create():
    return redirect(url_for('editor.tinymce',post_id=0))

@blueprint.route('/create', methods=['post'])
def create_post():
    title = request.form['title']
    content = request.form['editor']
    post_id = post_svc.create_post(title,content)
    return redirect(url_for('read.read',post_id=post_id))


@blueprint.route('/update/<int:post_id>', methods=['GET'])
def update_get(post_id: int):
    return redirect(url_for('editor.tinymce', post_id=post_id))


@blueprint.route('/update/<int:post_id>', methods=['post'])
def update_post(post_id: int):
    title = request.form['title']
    content = request.form['editor']
    post_svc.update_post(post_id,title,content)
    return redirect(url_for('read.read', post_id=post_id))


@blueprint.route('/delete/<int:post_id>', methods=["GET"])
def delete(post_id: int):
    post_svc.delete_post(post_id)
    return redirect(url_for('read.index'))
