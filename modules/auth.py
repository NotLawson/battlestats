# auth module
from modules.battletabs import BattleTabsClient
import json
from __main__ import db, influx
import random

TOKENS = {}

def generate_token(username):
    chars = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j',
             'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T',
             'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    while True:
            taken = False
            token=""
            i=0
            for i in range(20):
                token+=random.choice(chars)
                i+=1
            for i in TOKENS.keys():
                if token==TOKENS[i]:
                    taken = True
                    break
            if not taken:
                break
    TOKENS.update({username:token})
    return token

class User:
    def __init__(self, username, password, auth_token):
        self.username = username
        self.password = password
        self.token = auth_token
        self.client = BattleTabsClient(auth_token)

        info = self.get_self()
        self.id = info["me"]["id"]
        self.name = info["me"]["name"]
        self.email = info["me"]["email"]

        self.sync()

    def get_self(self):
        return self.client.query("{me {name\nemail\nid}}")
    
    def sync(self):
        q = '''{me {name email id stats {wins losses} enhancedStats} myLeagueProgress {trophies diamonds} avatarParts {definitionId} medals(userId: "'''+self.id+'''") {definitionId} customFleets {name slotIndex ships {definitionId skinId}}}'''
        data = self.client.query(q)

        self.name = data["me"]["name"]

        self.stats = {
            "wins":data["me"]["stats"]["wins"],
            "losses":data["me"]["stats"]["losses"],
            "currentStreak":data["me"]["enhancedStats"]["winningStreak"]["current"],
            "longestStreak":data["me"]["enhancedStats"]["winningStreak"]["longest"]
        }

        self.league = {
            "trophies":data["myLeagueProgress"]["trophies"],
            "diamonds":data["myLeagueProgress"]["diamonds"]
        }
        influx.update_league(self.username, self.league["trophies"])

        self.fleets = data["customFleets"]
        self.inventory = data["avatarParts"]
        self.medals = data["medals"]

    
    def __dict__(self):
        return {
            "username":self.username,
            "password":self.password,
            "token":self.token,
            "id":self.id,
            "name":self.name,
            "email":self.email
        }
    
def login(username, password):
    from __main__ import userdb
    user = userdb.get(username)
    if user==None:
        return "invalidusername"
    
    if user.password != password:
        return "invalidpassword"
    
    return generate_token(username)

def auth(token):
    for i in TOKENS.keys():
        if token == TOKENS[i]:
            username = i
            return username
    return None

class UserFromDict(User):
    def __init__(self, userdict):
        self.username = userdict["username"]
        self.password = userdict["password"]
        self.token = userdict["token"]
        self.client = BattleTabsClient(userdict["token"])
        self.id = userdict["id"]
        self.name = userdict["name"]
        self.email = userdict["email"]
        self.sync()

class UserDB(db.DB):
    def __init__(self):
        super().__init__("users")

        if self.redis.get("_idtousername")==None:
            self.redis.set("_idtousername", json.dumps({}))

    def find_username(self, id):
        try: return json.loads(self.redis.get("_idtousername"))[id]
        except KeyError: return "unknown"
    
    def set(self, key, value):
        self.redis.set(key, json.dumps(value.__dict__()))
    
    def get(self, key):
        resp = self.redis.get(key)
        if resp==None:
            return None
        return UserFromDict(json.loads(resp))