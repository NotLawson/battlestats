import redis, pickle, json
from auth import UserFromDict

class DB:
    def __init__(self, host):
        self.redis = redis.Redis(host=host, port=6379, db=0, decode_responses=True)
    
    def get(self, key):
        resp = self.redis.get(key)
        if resp==None:
            return None
        return pickle.loads(resp)
    
    def set(self, key, value):
        self.redis.set(key, pickle.dumps(value))

class UserDB(DB):
    def __init__(self):
        super().__init__("users")

    def set(self, key, value):
        self.redis.set(key, json.dumps(dict(value)))
    
    def get(self, key):
        resp = self.redis.get(key)
        if resp==None:
            return None
        return UserFromDict(json.loads(resp))