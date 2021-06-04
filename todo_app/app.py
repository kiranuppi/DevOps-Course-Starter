from flask import Flask, render_template, redirect, url_for, request

from todo_app.ViewModel import ViewModel
from todo_app.data.Trello import trello
from todo_app.flask_config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    trello.init()

    @app.route('/')
    def index():
        item_view_model = ViewModel(
            trello.get_list_items(), trello.get_current_sort_order())
        return render_template('index.html', view_model=item_view_model)

    @app.route('/', methods=['POST'])
    def add_item():
        app.logger.info('Adding new item on a card')
        trello.add_new_item(request.form['title'])
        return redirect('/')

    @app.route('/actions/<action>/<id>')
    def move_item(action, id):
        app.logger.info('Moving an item from ')
        if action in ['start', 'doing']:
            trello.update_to_inprogress(id)
        elif action == 'done':
            trello.update_to_done(id)

        return redirect('/')

    @app.route('/sortby/<sortby>')
    def sort_by(sortby):  # pylint:disable=unused-variable
        trello.set_current_sort_order(sortby)
        return redirect('/')

    return app
