import logging

import sys

sys.path.append("/opt/controlSystem")

import pymongo

logging.basicConfig(level=logging.INFO)
from repositories import devices as repo_devices
from repositories import heartbeats_devices as repo_heartbeats_device
import json
from threading import Thread
import random
import os
import time
import subprocess, platform

MIN_SLEEP = 60
MAX_SLEEP = 60 * 3


def save_heartbeat_response(device_id, device_name, device_ip, success=False):
    if success:
        action = "success"
        log = "heartbeat success"
    else:
        action = "failed"
        log = "heartbeat failed"
    repo_heartbeats_device.insert_heartbeat_device(device_id, device_name,
                                                   device_ip, action, log, success=success)

def thread_hearbeat_device(device_name, device_ip, device_id):
    logging.info("************ THREAD INIT: DEVICE - " + str(device_name) + " - IP - " + str(device_ip) + " **********")
    while True:
        logging.info("* THREAD REQUEST HEARTBEAT: DEVICE - " + device_name + " - IP - " + device_ip)
        # response = subprocess.check_output(
        #     "ping -{} 1 {}".format('n' if platform.system().lower() == "windows" else 'c', device_ip), shell=True)

        response = os.system("ping -{} 1 {}".format('n' if platform.system().lower() == "windows" else 'c', device_ip))

        response = response.decode()
        # logging.info(response)
        # if 'bytes=32' in response and 'Packets: Sent = 1, Received = 1, Lost = 0 (0% loss)' in response:
        if response == 0:
            logging.info(
                "** THREAD RESPONSE HEARTBEAT: DEVICE - " + device_name + " - IP - " + device_ip + " => SUCCESS!")
            save_heartbeat_response(device_id, device_name, device_ip, success=True)
        else:
            logging.info(
                "** THREAD RESPONSE HEARTBEAT: DEVICE - " + device_name + " - IP - " + device_ip + " => Failed!")
            save_heartbeat_response(device_id, device_name, device_ip, success=False)

        random_sleep = random.randint(MIN_SLEEP, MAX_SLEEP)
        logging.info("THREAD: DEVICE - " + device_name + " - IP - " + device_ip + " - SLEEPPING " + str(
            random_sleep) + " seconds")
        time.sleep(random_sleep)

if __name__ == "__main__":
    logging.info("Initializing POLLING HEARTBEATS SERVICE")
    all_devices = repo_devices.get_all_devices()

    threadlist = []
    for device in all_devices:
        device_name = device["name"]
        device_ip = device["IP"]
        device_id = device["_id"]["$oid"]
        threadlist.append(Thread(target=thread_hearbeat_device, args=(device_name, device_ip, device_id)))

    for t in threadlist:
        t.start()

    for t in threadlist:
        t.join()
