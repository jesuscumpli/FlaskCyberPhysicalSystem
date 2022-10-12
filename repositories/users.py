import datetime

from repositories.clientMongo import client, db

collection = db["users"]


def insert_user(username, salt, password):
    user_data = {
        "username": username, "salt": salt,
        "password": password,
        "register_date": datetime.datetime.now(),
        "login_date": datetime.datetime.now()
    }
    result = collection.insert_one(user_data)
    return result

def update_user_login_date(username):
    myquery = {"username": username}
    update_value = {"$set": {"login_date": datetime.datetime.now()}}
    collection.update_one(myquery, update_value)

def find_user_by_username(username):
    result = collection.find_one({"username": username})
    return result
