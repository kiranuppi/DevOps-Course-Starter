from flask import Flask, render_template, redirect, url_for, request, app

from todo_app.data.Trello import trello
from todo_app.flask_config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    def index():
        app.logger.info('Getting all cards from the board')
        items = trello.get_list_items()
        return render_template('index.html', items=items)

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

    if __name__ == '__main__':
        app.run()

    return app
