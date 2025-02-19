## from redis_console import *
## db.(...)

import redis
db = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)