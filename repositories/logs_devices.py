from repositories.clientMongo import client, db
import datetime
import json
from bson import json_util
import pymongo

collection = db["logs_devices"]

def insert_log_device(device_id, device_name, device_IP, action, log):
    device_data = {
        "device_id": device_id,
        "device_name": device_name,
        "device_IP": device_IP,
        "action": action,
        "log": log,
        "date": datetime.datetime.now()
    }
    result = collection.insert_one(device_data)
    return result

def get_all_logs_from_device(device_id):
    result = list(collection.find({"device_id": device_id}, sort=[('date', pymongo.DESCENDING)]))
    result = json.loads(json_util.dumps(result))
    return result

def get_last_log_device_from_device(device_id):
    result = collection.find_one({"device_id": device_id}, sort=[('date', pymongo.DESCENDING)])
    result = json.loads(json_util.dumps(result))
    return result