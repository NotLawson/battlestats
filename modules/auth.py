# auth module
from modules.battletabs import SelfDestructClient
from __main__ import userdb
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
    async def __init__(self, username, password, auth_token):
        self.username = username
        self.password = password
        self.token = auth_token

        info = self.get_self()
        self.id = info["me"]["id"]
        self.name = info["me"]["name"]
        self.email = info["me"]["email"]

    def get_self(self):
        return self.get_client().query("{me {name\nemail\nid}}")
    
    async def get_stats(self):
        stats = self.get_client().query("{me {stats {wins\nlosses}\nenhancedStats}}")
        return {
            "wins":stats["me"]["stats"]["wins"],
            "losses":stats["me"]["stats"]["losses"],
            "currentStreak":stats["me"]["enhancedStats"]["winningStreak"]["current"],
            "longestStreak":stats["me"]["enhancedStats"]["winningStreak"]["longest"]
        }
    
    def get_league(self):
        league = self.get_client().query("{myLeagueProgress {trophies\ndiamonds}}")
        return {
            "trophies":league["myLeagueProgress"]["trophies"],
            "diamonds":league["myLeagueProgress"]["diamonds"]
        }
    
    def get_avatar_inventory(self):
        return self.get_client().query("{avatarParts {definitionId}}")
    
    def get_medals(self):
        return self.get_client().query('''{medals(userId: "'''+self.id+'''") {definitionId}}''')
    
    def get_fleets(self):

        return self.get_client().query("{customFleets {name\nslotIndex\nships {definitionId\nskinId}}}")
    
    def get_client(self):
        return SelfDestructClient(self.token)
    
def login(username, password):
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