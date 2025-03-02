# auth module
from modules.battletabs import BattleTabsClient
import json
from __main__ import db
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
                if token==TOKENS[i]["token"]:
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

    def get_self(self):
        return self.client.query("{me {name\nemail\nid}}")
    
    def get_stats(self):
        stats = self.client.query("{me {stats {wins\nlosses}\nenhancedStats}}")
        return {
            "wins":stats["me"]["stats"]["wins"],
            "losses":stats["me"]["stats"]["losses"],
            "currentStreak":stats["me"]["enhancedStats"]["winningStreak"]["current"],
            "longestStreak":stats["me"]["enhancedStats"]["winningStreak"]["longest"]
        }
    
    def get_league(self):
        league = self.client.query("{myLeagueProgress {trophies\ndiamonds}}")
        return {
            "trophies":league["myLeagueProgress"]["trophies"],
            "diamonds":league["myLeagueProgress"]["diamonds"]
        }
    
    def get_avatar_inventory(self):
        return self.client.query("{avatarParts {definitionId}}")
    
    def get_medals(self):
        return self.client.query('''{medals(userId: "'''+self.id+'''") {definitionId}}''')
    
    def get_fleets(self):

        return self.client.query("{customFleets {name\nslotIndex\nships {definitionId\nskinId}}}")
    
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
        if token == TOKENS[i]["token"]:
            username = TOKENS[i]["username"]
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


class UserDB(db.DB):
    def __init__(self):
        super().__init__("users")

    def set(self, key, value):
        self.redis.set(key, json.dumps(dict(value)))
    
    def get(self, key):
        resp = self.redis.get(key)
        if resp==None:
            return None
        return UserFromDict(json.loads(resp))