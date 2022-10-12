from repositories.clientMongo import client, db
import datetime

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
    result = list(collection.find({"device_id": device_id}))
    return result