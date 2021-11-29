import os
from flask import Flask, render_template, request, redirect
from todo_app.dbconnection_manager import *
from todo_app.view import ViewModel
from todo_app.models.card import Card

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')

    #error handling for 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", error='not found!')

    # @app.route('/contact')
    # def contact():
    #     return render_template('contact.html')

    #default
    @app.route('/', methods=['GET'])
    def get_index():
        cardslist = []
        mongo = DB_Connection_Manager()
        items = mongo.get_AllItems()

        for item in items:
            cardslist.append(Card(item))

        item_view_model = ViewModel(cardslist)
        return render_template('index.html', view_model=item_view_model)

    # @app.route('/getpreviousdonetasks', methods=['GET'])
    # def get_previous_done_tasks():
    #     cardslist = []
    #     mongo = MongoDBClient()
    #     qry = {
    #         "status": "Done",
    #         "dateLastActivity": {"$lt": datetime.datetime.strptime((datetime.date.today()).strftime("%Y-%m-%d"), '%Y-%m-%d')}
    #     }
    #     items = mongo.get_qryItems(qry)
    #     for item in items:
    #         cardslist.append(Card(item))
    #     item_view_model = ViewModel(cardslist)
    #     return render_template('today_done_task.html', view_model=item_view_model)

    
    # @app.route('/gettodaydonetasks', methods=['GET'])
    # def get_today_done_tasks():
    #     cardslist = []
    #     mongo = MongoDBClient()
    #     qry = {
    #         "status": "Done",
    #         "dateLastActivity": datetime.datetime.strptime((datetime.date.today()).strftime("%Y-%m-%d"), '%Y-%m-%d')
    #     }
    #     items = mongo.get_qryItems(qry)
    #     for item in items:
    #         cardslist.append(Card(item))
    #     item_view_model = ViewModel(cardslist)
    #     return render_template('today_done_task.html', view_model=item_view_model)

    # new task
    @app.route('/new', methods=['GET'])
    def getnew_post():
        return render_template('new_task.html')

    @app.route('/', methods=['POST'])
    def post_index():
        mongo = DB_Connection_Manager()
        response = mongo.create_task(
            name = request.form['title'],
            due = request.form['duedate'],
            desc = request.form['descarea']
        )
        
        if (str(response) != ""):
            return redirect('/')
        else:
            return render_template("error.html",error="Task creation failed ")

    # edit task
    @app.route('/edit/<id>', methods=['GET'])
    def get_edit(id):
        mongo = DB_Connection_Manager()
        item = mongo.get_task(id=id)
        if (str(item) != ""):
            item_info = Card(item)
            return render_template('edit.html', task=item_info)
        else:
            return render_template("error.html", error="Can not retrieve task information")

    @app.route('/edit/<id>', methods=['POST'])
    def post_edit(id):
        mongo = DB_Connection_Manager()
        response= mongo.update_task(
            id = id,
            name = request.form['title'],
            desc = request.form['descarea'],
            due = request.form['duedate'],
            status = request.form['status']
        )
        if (str(response) != ""):
            return redirect('/')
        else:
            return render_template("error.html", error="Task update failed !")

    # delete task
    @app.route('/delete/<id>')
    def delete(id):
        mongo = DB_Connection_Manager()
        response = mongo.delete_task(id=id)
        if str(response) != "":
            return redirect('/')
        else:
            return render_template("error.html",error="failed to delete task!")      

    return app

