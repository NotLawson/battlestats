## Communication library for the runners
import redis
import threading
import queue
import json

class RunnerClient:
    def __init__(self, host="systems"):
        self.redis = redis.Redis(host=host, port=6379, db=0)
        self.event_queue = queue.Queue()
        self.pump_thread = threading.Thread(target=self.pump, daemon=True)
        self.pump_thread.start()
    def pump(self):
        """
        Push messages to redis from the event queue.
        """
        while True:
            event = self.event_queue.get(True, None)
            self.redis.publish("event", json.dumps(event))
            self.event_queue.task_done()
    
    def event(self, event):
        """
        Push an event to the event queue.
        """
        self.event_queue.put(event)
