import datetime

from repositories.clientMongo import client, db
from bson.objectid import ObjectId
from bson import json_util
import json

collection = db["devices"]

def insert_device(name, type, IP, public_key_bytes, longitude, latitude, by_username):
    device_data = {
        "name": name,
        "type": type,
        "IP": IP,
        "public_key": public_key_bytes,
        "longitude": longitude,
        "latitude": latitude,
        "last_update": datetime.datetime.now(),
        "last_update_by": by_username,
        "register_date": datetime.datetime.now(),
        "register_date_by": by_username
    }
    result = collection.insert_one(device_data)
    return result

def update_device(device_id, name, type, IP, public_key_bytes, longitude, latitude, by_username):
    device_data = {
        "name": name,
        "type": type,
        "IP": IP,
        "longitude": longitude,
        "latitude": latitude,
        "last_update": datetime.datetime.now(),
        "last_update_by": by_username,
    }
    if public_key_bytes:
        device_data["public_key"] = public_key_bytes
    query = {"_id": ObjectId(device_id)}
    update_value = {"$set": device_data}
    result = collection.update_one(query, update_value)
    return result

def delete_device(device_id):
    result = collection.delete_one({"_id": ObjectId(device_id)})
    return result

def get_all_devices():
    result = list(collection.find())
    result = json.loads(json_util.dumps(result))
    return result

def get_device_by_id(device_id):
    result = collection.find_one({"_id": ObjectId(device_id)})
    result = json.loads(json_util.dumps(result))
    return result

def get_device_by_IP(IP):
    result = collection.find_one({"IP": IP})
    result = json.loads(json_util.dumps(result))
    return result