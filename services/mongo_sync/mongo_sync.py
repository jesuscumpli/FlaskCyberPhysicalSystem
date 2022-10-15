import time
from datetime import datetime

import sys
sys.path.append("/opt/controlSystem")

from pymongo import MongoClient
import os
import subprocess
import logging
logging.basicConfig(level=logging.INFO)

HOST_MONGO = "192.168.1.1"
PORT_MONGO = 27017
HOST_LOCAL = "localhost"
PORT_LOCAL = 27017
DATABASE = "control_system"
SLEEP_TIME = 60 * 5

# client_host = MongoClient(HOST_MONGO, PORT_MONGO)
# db_host = client_host[DATABASE]
#
# client_local = MongoClient(HOST_LOCAL, PORT_LOCAL)
# db_local = client_local[DATABASE]

while True:
    try:
        logging.info("INICIO SERVICIO - SYNC MONGODB")

        logging.info("**** MONGODUMP ***")
        cmd = "mongodump --host=" + HOST_LOCAL + " --port=" + str(
            PORT_LOCAL) + " --out=/opt/controlSystem/services/mongo_sync/mongodump --db=" + DATABASE
        temp = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output = str(temp.communicate())
        logging.info("SALIDA MONGODUMP: " + str(output))

        logging.info("**** MONGORESTORE ***")
        cmd = "mongorestore --host=" + HOST_MONGO + " --port=" + str(
            PORT_MONGO) + " /opt/controlSystem/services/mongo_sync/mongodump"
        temp = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output = str(temp.communicate())
        logging.info("SALIDA MONGORESTORE: " + str(output))
    except Exception as e:
        logging.exception("ERROR: " + str(e))

    logging.info("Durmiendo servicio...")
    time.sleep(SLEEP_TIME)
