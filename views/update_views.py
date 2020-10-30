import flask
from flask import redirect, url_for
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

from infrastructure.view_modifiers import response
from services.post_service import create_post, update_post, delete_post
blueprint = flask.Blueprint('update', __name__, template_folder='templates')


class PostForm(Form):
    """Form to update posts."""
    title = StringField("Title", [DataRequired()])
    content = TextField("Content", [DataRequired()])
    submit = SubmitField('Submit')

@blueprint.route('/create', methods=['Get', 'POST'])
@response(template_file='update/create.html')
def create():
    form = PostForm()
    if form.validate_on_submit():
        new_id = create_post(form.title.data, form.content.data)
        return redirect(url_for('read.read', post_id=new_id))
    return {'form' : form}

@blueprint.route('/update/<int:post_id>', methods=('GET', 'POST'))
@response(template_file='update/update.html')
def update(post_id: int):
    form = PostForm()
    if form.validate_on_submit():
        update_post(post_id, form.title.data, form.content.data)
        return redirect(url_for('read.read', post_id=post_id))
    return {'form' : form, 'id' : post_id}


@blueprint.route('/delete/<int:post_id>', methods=["GET"])
def delete(post_id: int):
    delete_post(post_id)
    return redirect(url_for('read.index'))