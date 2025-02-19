import redis, pickle


class UserDB:
    def __init__(self):
        self.redis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    
    def get(self, key):
        resp = self.redis.get(key)
        if resp==None:
            return None
        return pickle.loads(resp)
    
    def set(self, key, value):
        self.redis.set(key, pickle.dumps(value))