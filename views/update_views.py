import flask
from flask import redirect, url_for
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

from infrastructure.view_modifiers import response

blueprint = flask.Blueprint('update', __name__, template_folder='templates')


class PostForm(Form):
    """Form to update posts."""
    title = StringField("Title", [DataRequired()])
    content = TextField("Content", [DataRequired()])
    submit = SubmitField('Submit')

@blueprint.route('/update/<int:post_id>', methods=('GET', 'POST'))
@response(template_file='update/update.html')
def update(post_id: int):
    form = PostForm()
    if form.validate_on_submit():
        return redirect(url_for('read.read', post_id=post_id))
    return {'form' : form, 'id' : post_id}

