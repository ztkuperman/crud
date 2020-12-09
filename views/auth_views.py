from flask import Blueprint, request, session, abort, redirect, url_for,flash
from infrastructure.view_modifiers import response
import services.user_service as user_svc
import services.auth_service as auth_svc
blueprint = Blueprint("auth", __name__, template_folder="templates")

@blueprint.route("/adminsignup", methods=['GET'])
@response(template_file="auth/adminsignup.html")
def admin_signup_get():
    return {'csrf_token':user_svc.csrf_new_token()}

@blueprint.route("/adminsignup", methods=['POST'])
@response(template_file="auth/adminsignup.html")
def admin_signup_post():
    form = request.form
    init_key = open('initialization_key.txt').read()
    if init_key == form['init_key']:
        flash("Initialization Confirmed.")
        csrf_valid = user_svc.csrf_validate(csrf_token)
        msg = user_svc.add_new_user(name,email,password)
        if msg == "" and csrf_valid:
            msg = user_svc.login_user(form['name'], form['password'])
            return redirect(url_for('read.index'))
        else:
            flash(msg)
    else:
        flash("Initializaton Key Error.")
        return {"csrf_token":user_svc.csrf_new_token()}

@blueprint.route('/admin', methods=['GET'])
@response(template_file="auth/admin.html")
def admin_page_get():
    # This is necessary to interface with jinja, which can't do the dict comp right
    auth_data = user_svc.user_authorization_get()
    auth_data = [[name,role,status] for name,[role,status] in auth_data.items()]
    return {"auth_data":auth_data}


@blueprint.route('/admin', methods=['POST'])
@response(template_file="auth/admin.html")
def admin_page_post():
    form = request.form
    new_auth_data = {row[0]:[row[1],row[2]] for row in form.listvalues()}
    print(new_auth_data)
    msg = user_svc.user_authorization_update(new_auth_data)
    flash(msg)
    return redirect(url_for("auth.admin_page_get"))

@blueprint.before_app_request
def authorization_check():
    user = session.get('username')
    method = request.method
    route = request.path
    if not auth_svc.authorize_route(user, method, route):
        abort(403)


