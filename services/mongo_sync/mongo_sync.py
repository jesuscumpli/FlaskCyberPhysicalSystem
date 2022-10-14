import time
from datetime import datetime
from pymongo import MongoClient
import os
import subprocess

HOST_MONGO = "192.168.1.1"
SLEEP_TIME = 60*5

client_host = MongoClient(HOST_MONGO, 27017)
db_host = client_host["control_system"]

client_local = MongoClient("localhost", 27017)
db_local = client_local["control_system"]


while True:
    cmd = "mongodump --host=localhost --port=27017 --out=/opt/controlSystem/services/mongo_sync/mongodump"
    temp = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    # get the output as a string
    output = str(temp.communicate())
    print(output)
    time.sleep(SLEEP_TIME)