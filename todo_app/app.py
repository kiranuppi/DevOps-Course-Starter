from flask import Flask, render_template, request

from todo_app.data import session_items
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = session_items.get_items()
    sorted_items = sorted(items, key=lambda i: i['status'], reverse=True)
    return render_template('index.html', items=sorted_items)


@app.route('/addItem', methods=['POST'])
def add_items():
    new_item = request.form.get('todoitem')
    session_items.add_item(new_item)
    return index()


@app.route('/completeItem', methods=['POST'])
def complete_items():
    position_id = request.form['complete']
    session_items.mark_as_complete_item(position_id)
    return index()


@app.route('/removeItem', methods=['POST'])
def remove_items():
    remove_item = request.form.get('remove_todoitem')
    session_items.remove_item(remove_item)
    return index()


if __name__ == '__main__':
    app.run()
