# Service worker to handle the graphql resquests
import gql
from threading import Thread
from queue import Queue
from time import sleep
from __main__ import userdb

def worker(queue):
    while True:
        item = queue.get()
        if item["type"]=="sync":
            user = userdb.get(item["username"])
            user.sync()
            userdb.set(item["username"], user)
        sleep(1)

def loadbalancer(main_queue, scale):
    queues = [Queue() for i in range(scale)]
    threads = [Thread(target=worker, args=(queues[i],)) for i in range(scale)]
    for thread in threads:
        thread.start()
    while True:
        for queue in queues:
            item = main_queue.get()
            queue.put(item)

def start(main_queue, scale):
    print("Starting Loadbalancer with scale", scale)
    Thread(target=loadbalancer, args=(main_queue, scale)).start()