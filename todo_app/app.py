import os, requests
from flask import Flask, redirect, url_for, session, request
from todo_app.managers.dbconnection_manager import *
from todo_app.managers.user_manager import *
from todo_app.models.view import View
from todo_app.models.card import Card
from todo_app.models.user import User
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

    client_id = os.environ['GITHUB_CLIENT_ID']
    client_secret = os.environ['GITHUB_CLIENT_SECRET']
    base_url = "https://api.github.com"
    authorization_url = "https://github.com/login/oauth/authorize"
    token_endpoint = "https://github.com/login/oauth/access_token"

    client = WebApplicationClient(client_id)
    todo = DB_Connection_Manager()
    usermanager = DB_User_Manager()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return UserToLogin(user_id)

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(url_for('login'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
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

        if token_response.status_code != 200:
            return redirect(url_for('login'))

        json_data = token_response.content.decode('utf8').replace("'", '"')
        # Parse the tokens!
        client.parse_request_body_response(json_data)
        userinfo_endpoint = "{}/user".format(base_url)
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.ok:
            account_info_json = userinfo_response.json()
            currentUserName = str(account_info_json['login'])
            login_user(UserToLogin(currentUserName))

            if usermanager.get_totalusercount() == 0:
                usermanager.create_user(username=currentUserName, role="admin")

            if (usermanager.get_totalusercount() > 0) and (
                    usermanager.get_findusercount(qry={"username": currentUserName}) == 0):
                usermanager.create_user(username=currentUserName, role="read")

        return redirect(url_for('get_index'))

    @app.route('/', methods=['GET'])
    @login_required
    def sendhome():
        return redirect(url_for('get_index'))

    # error handling for 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", error='not found!')


    # default
    @app.route('/home', methods=['GET'])
    @login_required
    def get_index():
        cardslist = []
        items = todo.get_AllItems()
        if (app.config['LOGIN_DISABLED']):
            userRole = False
        else:
            userRole = usermanager.IsDisable()

        for item in items:
            cardslist.append(Card(item))
        item_view_model = View(cardslist)
        return render_template('index.html', view_model=item_view_model, strRole=userRole)

    # new task
    @app.route('/new', methods=['GET'])
    @login_required
    @usermanager.hasWritePermission
    def getnew_post():
        return render_template('new_task.html')

    @app.route('/', methods=['POST'])
    @login_required
    @usermanager.hasWritePermission
    def post_index():
        mongo = DB_Connection_Manager()
        response = mongo.create_task(
            name=request.form['title'],
            due=request.form['duedate'],
            desc=request.form['descarea']
        )

        if (str(response) != ""):
            return redirect('/home')
        else:
            return render_template("error.html", error="Task creation failed ")

    # edit task
    @app.route('/edit/<id>', methods=['GET'])
    @login_required
    @usermanager.hasWritePermission
    def get_edit(id):
        item = todo.get_task(id=id)
        if (str(item) != ""):
            item_info = Card(item)
            return render_template('edit.html', task=item_info)
        else:
            return render_template("error.html", error="Can not retrieve task information")

    @app.route('/edit/<id>', methods=['POST'])
    @login_required
    @usermanager.hasWritePermission
    def post_edit(id):
        response = todo.update_task(
            id=id,
            name=request.form['title'],
            desc=request.form['descarea'],
            due=request.form['duedate'],
            status=request.form['status']
        )
        if (str(response) != ""):
            return redirect('/home')
        else:
            return render_template("error.html", error="Task update failed !")

    # delete task
    @app.route('/delete/<id>')
    @login_required
    @usermanager.hasWritePermission
    def delete(id):
        response = todo.delete_task(id=id)
        if str(response) != "":
            return redirect('/home')
        else:
            return render_template("error.html", error="failed to delete task!")

    ############# UserManagement ##########################
    @app.route('/usermanager', methods=['GET'])  # portal
    @login_required
    @usermanager.hasRoleAdmin
    def get_usermanager():
        user_list = []
        items = usermanager.get_AllUsers()
        for item in items:
            user_list.append(User(item))
        item_view_model = View(user_list)
        return render_template('userManager.html', view_model=item_view_model)

    @app.route('/edituser/<id>', methods=['GET'])  # Edit user
    @login_required
    @usermanager.hasRoleAdmin
    def get_edituser(id):
        item = usermanager.get_user(id=id)
        if (str(item) != ""):
            item_info = User(item)
            return render_template('editUser.html', user=item_info)
        else:
            return render_template("error.html", error="failed to obtain user info!")

    @app.route('/edituser/<id>', methods=['POST'])  # Edit user
    @login_required
    @usermanager.hasRoleAdmin
    def post_edituser(id):
        response = usermanager.update_user(
            id=id,
            username=request.form['username'],
            role=request.form['role']
        )
        if (str(response) != ""):
            return redirect('/usermanager')
        else:
            return render_template("error.html", error="failed to update user!")

    @app.route('/deleteuser/<id>')  # delete user
    @login_required
    @usermanager.hasRoleAdmin
    def deleteuser(id):
        response = usermanager.delete_user(id=id)
        if str(response) != "":
            return redirect('/usermanager')
        else:
            return render_template("error.html", error="failed to delete user!")

    return app
