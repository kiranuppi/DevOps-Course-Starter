import os, ssl, pymongo, functools
from bson.objectid import ObjectId
from flask import render_template, current_app
from flask_login import current_user


class Connection():
    def __init__(self):
        self.mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
        self.mongo_collection_name = os.environ['MONGODB_COLLECTION_NAME']
        self.client = pymongo.MongoClient(self.mongo_connection_string, ssl_cert_reqs=ssl.CERT_NONE)
        self.mongo_db = self.client.todo_app
        self.collection = self.mongo_db.users


class DB_User_Manager(Connection):
    def get_totalusercount(self):
        return self.collection.find().count()

    def get_findusercount(self, qry):
        if qry != '':
            return self.collection.find(qry).count()

    def get_AllUsers(self):
        return self.collection.find()

    def get_qryItems(self, qry):
        if qry != '':
            return self.collection.find(qry)

    def create_user(self, username, role):
        post = {
            "username": username,
            "role": role
        }
        return self.collection.insert_one(post).inserted_id

    def delete_user(self, id):
        return self.collection.delete_one({"_id": ObjectId(id)})

    def update_user(self, id, username, role):
        post = {
            "username": username,
            "role": role
        }
        return self.collection.update_one({"_id": ObjectId(id)}, {"$set": post})

    def get_user(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def IsDisable(self):
        disable = True
        if not (current_user.id is None):
            results = self.collection.find({"username": current_user.id})
            for item in results:
                if (item['role'] == 'write') or (item['role'] == 'admin'):
                    disable = False
        return disable

    def hasRoleAdmin(self, func):
        @functools.wraps(func)
        def wrapper_hasRoleAdmin(*args, **kwargs):
            results = self.collection.find({"username": current_user.id})
            if not (results is None):
                for item in results:
                    if item['role'] != 'admin':
                        return render_template("access_error.html", error="insufficient privileges!")
                return func(*args, **kwargs)
            else:
                return render_template("error.html", error="Contact support for help.")

        return wrapper_hasRoleAdmin

    def hasWritePermission(self, func):
        @functools.wraps(func)
        def wrapper_hasWritePermission(*args, **kwargs):
            if current_app.config["LOGIN_DISABLED"]:
                return func(*args, **kwargs)
            results = self.collection.find({"username": current_user.id})
            if not (results is None):
                for item in results:
                    if item['role'] == 'read':
                        return render_template("access_error.html", error="insufficient privileges!")
                return func(*args, **kwargs)
            else:
                return render_template("error.html", error="Contact support for help.")

        return wrapper_hasWritePermission
