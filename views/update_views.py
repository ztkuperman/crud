import flask
from flask import redirect, url_for, request, session, flash

from infrastructure.view_modifiers import response
import services.post_service as post_svc
import services.user_service as user_svc

blueprint = flask.Blueprint('update', __name__, template_folder='templates')


@blueprint.route('/create', methods=['Get',])
@response(template_file='update/create.html')
def create():
    return redirect(url_for('editor.tinymce',post_id=0))

@blueprint.route('/create', methods=['post'])
def create_post():
    if user_svc.csrf_validate(request.form.get('csrf_token')):
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
    if user_svc.csrf_validate(request.form.get('csrf_token')):
        title = request.form['title']
        content = request.form['editor']
        post_svc.update_post(post_id,title,content)
        flash(f"Save successful. Post #{post_id} Updated.")
    else:
        flash('Error: Save unsuccessful')
    return redirect(url_for('editor.tinymce', post_id=post_id))


@blueprint.route('/delete', methods=["POST"])
def delete():
    if user_svc.csrf_validate(request.form.get('csrf_token')):
        post_svc.delete_post(request.form.get('post_id'))
    return redirect(url_for('read.index'))

@blueprint.route('/publish', methods=['POST'])
def publish():
    post_id = request.form.get('post_id')
    pub_status = request.form.get('pub_status')
    if user_svc.csrf_validate(request.form.get('csrf_token')):
        statuses = post_svc.update_publish(post_id, pub_status)
    # Redirect to the most public status level
    if "public" in statuses:
        return redirect(url_for('read.index'))
    elif "draft" in statuses:
        return redirect(url_for('read.drafts'))

