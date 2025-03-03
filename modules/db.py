import redis, pickle
from influxdb import InfluxDBClient

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

class InfluxDB:
    def __init__(self):
        self.client = InfluxDBClient(host='influxdb', port=8086)
        try: self.client.create_database('battletabs')
        except: pass
        self.client.switch_database('battletabs')

    def get_league(self, username):
        query = f'SELECT "league" FROM "battletabs"'
        resp = self.client.query(query)
        user_league = resp.get_points(tags={'username': username})
        return user_league
    
    def update_league(self, username, league):
        json_body = [
            {
                "measurement": "league",
                "tags": {
                    "username": username
                },
                "fields": {
                    "league": league
                }
            }
        ]
        self.client.write_points(json_body)
    