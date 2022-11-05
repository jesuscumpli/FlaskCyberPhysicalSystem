from repositories.clientMongo import client, db
import datetime
import json
from bson import json_util
import pymongo

collection = db["heartbeats_devices"]

def insert_heartbeat_device(device_id, device_name, device_IP, action, log, success=True):
    date = datetime.datetime.now()
    device_data = {
        "device_id": device_id,
        "device_name": device_name,
        "device_IP": device_IP,
        "action": action,
        "success": success,
        "log": log,
        "date": date
    }
    result = collection.insert_one(device_data)
    return result

def get_all_heartbeats_from_device(device_id):
    result = list(collection.find({"device_id": device_id}))
    result = json.loads(json_util.dumps(result))
    return result

def get_all_failed_heartbeats_from_device(device_id):
    result = list(collection.find({"device_id": device_id, "success": False}))
    result = json.loads(json_util.dumps(result))
    return result

def get_all_success_heartbeats_from_device(device_id):
    result = list(collection.find({"device_id": device_id, "success": True}))
    result = json.loads(json_util.dumps(result))
    return result

def get_last_heartbeat_from_device(device_id):
    result = collection.find_one({"device_id": device_id}, sort=[('date', pymongo.DESCENDING)])
    result = json.loads(json_util.dumps(result))
    return result