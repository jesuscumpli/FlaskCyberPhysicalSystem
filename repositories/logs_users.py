from repositories.clientMongo import client, db
import datetime

collection = db["logs_users"]

def insert_log_user(username, action, log):
    device_data = {
        "username": username,
        "action": action,
        "log": log,
        "date": datetime.datetime.now()
    }
    result = collection.insert_one(device_data)
    return result

def get_all_logs_user():
    result = collection.find()
    return result