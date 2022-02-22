import os, requests
from flask import Flask, redirect, url_for, session, request
from todo_app.managers.DbConnectionManager import *
from todo_app.managers.UserManager import *
from todo_app.models.view import View
from todo_app.models.card import Card
from todo_app.models.user import User

from loggly.handlers import HTTPSHandler
from logging import Formatter

# Login
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


class UserToLogin(UserMixin):
    def __init__(self, id):
        self.id = id


def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
        app.logger.addHandler(handler)

    client_id = os.environ['GITHUB_CLIENT_ID']
    client_secret = os.environ['GITHUB_CLIENT_SECRET']
    base_url = "https://api.github.com"
    authorization_url = "https://github.com/login/oauth/authorize"
    token_endpoint = "https://github.com/login/oauth/access_token"

    client = WebApplicationClient(client_id)
    todo = DbConnectionManager()
    user_manager = DbUserManager()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        app.logger.debug("Loading user for login......")
        return UserToLogin(user_id)

    @login_manager.unauthorized_handler
    def unauthenticated():
        app.logger.debug("User is not authenticated, redirect to login......")
        return redirect(url_for('login'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        app.logger.info("User logged out successfully")
        session.clear()
        return redirect("https://github.com/logout")

    @app.route("/login")
    def login():
        request_uri = client.prepare_request_uri(
            authorization_url,
            redirect_uri=request.base_url + "/callback",
            scope=None,
        )
        return redirect(request_uri)

    @app.route("/login/callback")
    def callback():
        code = request.args.get("code")

        # Prepare and send request to get tokens!
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code,
        )

        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(client_id, client_secret),
        )
        app.logger.debug("Token url:", token_url)
        if token_response.status_code != 200:
            app.logger.error("Failed to get Auth Token, redirecting to login screen")
            return redirect(url_for('login'))

        json_data = token_response.content.decode('utf8').replace("'", '"')
        # Parse the tokens!
        client.parse_request_body_response(json_data)
        userinfo_endpoint = "{}/user".format(base_url)

        app.logger.debug("User info endpoint : %s", userinfo_endpoint)
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.ok:
            account_info_json = userinfo_response.json()
            current_user_name = str(account_info_json['login'])
            login_user(UserToLogin(current_user_name))

            if user_manager.get_total_user_count() == 0:
                user_manager.create_user(username=current_user_name, role="admin")
                app.logger.info("New user: %s with ADMIN role has been created", current_user_name)

            if (user_manager.get_total_user_count() > 0) and (
                    user_manager.get_find_user_count(qry={"username": current_user_name}) == 0):
                user_manager.create_user(username=current_user_name, role="read")
                app.logger.info("New user: %s with READ role has been create", current_user_name)

        app.logger.info("User: %s logged in successfully", current_user_name)
        return redirect(url_for('get_index'))

    @app.route('/', methods=['GET'])
    @login_required
    def sendhome():
        app.logger.debug("Login successful, redirecting to home page")
        return redirect(url_for('get_index'))

    # error handling for 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", error='not found!')

    # default
    @app.route('/home', methods=['GET'])
    @login_required
    def get_index():
        cards_list = []
        items = todo.get_all_items()
        if (app.config['LOGIN_DISABLED']):
            app.logger.debug("Login disabled, hence no authentication flow needed.")
            user_role = False
        else:
            user_role = user_manager.is_disable()

        for item in items:
            cards_list.append(Card(item))
        item_view_model = View(cards_list)
        return render_template('index.html', view_model=item_view_model, strRole=user_role)

    # new task
    @app.route('/new', methods=['GET'])
    @login_required
    @user_manager.has_write_permission
    def getnew_post():
        return render_template('new_task.html')

    @app.route('/', methods=['POST'])
    @login_required
    @user_manager.has_write_permission
    def post_index():
        mongo = DbConnectionManager()
        response = mongo.create_task(
            name=request.form['title'],
            due=request.form['duedate'],
            desc=request.form['descarea']
        )

        if (str(response) != ""):
            app.logger.info("New Todo item : %s has been created", request.form['title'], user_id)
            return redirect('/home')
        else:
            app.logger.error("Failed to create new TODO item: %s", request.form['title'])
            return render_template("error.html", error="Task creation failed ")

    # edit task
    @app.route('/edit/<id>', methods=['GET'])
    @login_required
    @user_manager.has_write_permission
    def get_edit(id):
        item = todo.get_task(id=id)
        if (str(item) != ""):
            item_info = Card(item)
            app.logger.info("Task : %s is being edited", item_info.name)
            return render_template('edit.html', task=item_info)
        else:
            app.logger.error("Can not retrieve task information")
            return render_template("error.html", error="Can not retrieve task information")

    @app.route('/edit/<id>', methods=['POST'])
    @login_required
    @user_manager.has_write_permission
    def post_edit(id):
        response = todo.update_task(
            id=id,
            name=request.form['title'],
            desc=request.form['descarea'],
            due=request.form['duedate'],
            status=request.form['status']
        )
        if (str(response) != ""):
            app.logger.info("%s Task Updated Successfully", request.form['title'])
            return redirect('/home')
        else:
            app.logger.error(" %s Task update failed !", request.form['title'])
            return render_template("error.html", error="Task update failed !")

    # delete task
    @app.route('/delete/<id>')
    @login_required
    @user_manager.has_write_permission
    def delete(id):
        response = todo.delete_task(id=id)
        if str(response) != "":
            app.logger.info("Task deleted successfully !")
            return redirect('/home')
        else:
            app.logger.error("Failed to delete the task")
            return render_template("error.html", error="failed to delete task!")

    ############# UserManagement ##########################
    @app.route('/usermanager', methods=['GET'])  # portal
    @login_required
    @user_manager.has_role_admin
    def get_user_manager():
        user_list = []
        items = user_manager.get_all_users()
        for item in items:
            user_list.append(User(item))
        item_view_model = View(user_list)
        return render_template('userManager.html', view_model=item_view_model)

    @app.route('/edituser/<id>', methods=['GET'])  # Edit user
    @login_required
    @user_manager.has_role_admin
    def get_edituser(id):
        item = user_manager.get_user(id=id)
        if (str(item) != ""):
            item_info = User(item)
            app.logger.info("User: %s is being edited", item.name)
            return render_template('editUser.html', user=item_info)
        else:
            app.logger.error("Failed to obtain user info!")
            return render_template("error.html", error="failed to obtain user info!")

    @app.route('/edituser/<id>', methods=['POST'])  # Edit user
    @login_required
    @user_manager.has_role_admin
    def post_edituser(id):
        response = user_manager.update_user(
            id=id,
            username=request.form['username'],
            role=request.form['role']
        )
        if (str(response) != ""):
            app.logger.info("User : %s updated successfully!", request.form['username'])
            return redirect('/usermanager')
        else:
            app.logger.error("Failed to update user : %s", request.form['username'])
            return render_template("error.html", error="failed to update user!")

    @app.route('/deleteuser/<id>')  # delete user
    @login_required
    @user_manager.has_role_admin
    def deleteuser(id):
        response = user_manager.delete_user(id=id)
        if str(response) != "":
            app.logger.info("User: %s deleted successfully", id)
            return redirect('/usermanager')
        else:
            app.logger.error("Failed to delete user id : %s", id)
            return render_template("error.html", error="failed to delete user!")

    return app
