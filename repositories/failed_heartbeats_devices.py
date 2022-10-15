from repositories.clientMongo import client, db
import datetime
import json
from bson import json_util

collection = db["failed_heartbeats_devices"]

def insert_failed_heartbeat_device(device_id, device_name, device_IP, action, log):
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

def get_all_failed_heartbeats_from_device(device_id):
    result = list(collection.find({"device_id": device_id}))
    result = json.loads(json_util.dumps(result))
    return result