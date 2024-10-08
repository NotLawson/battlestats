from flask import Flask, render_template, request
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json


app = Flask(__name__)
API = "https://battletabs.fly.dev/graphql"


# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url=API)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

class PlayerData:
    def __init__(self, resp):
        #self.json = json.loads(resp)
        self.json = resp

        self.name = self.json["userByShortId"]["name"]
        self.trophies = self.json["userByShortId"]["stats"]["lifetimeTrophies"]
        self.wins = self.json["userByShortId"]["stats"]["wins"]
        self.losses = self.json["userByShortId"]["stats"]["losses"]
        self.wr = int(round(self.wins/(self.wins+self.losses), 2)*100)

        self.current_ws = self.json["userByShortId"]["enhancedStats"]["winningStreak"]["current"]
        self.longest_ws = self.json["userByShortId"]["enhancedStats"]["winningStreak"]["longest"]

        self.turns = self.json["userByShortId"]["enhancedStats"]["turns"]["taken"]


class TestingPlayerData(PlayerData):
    def __init__(self):
        resp = {
            "userByShortId":{
                "name":"Testing User",
                "stats":{
                    "lifetimeTrophies":10000,
                    "wins":100,
                    "losses":100,
                },
                "enhancedStats":{
                    "winningStreak":{
                        "current":11,
                        "longest":32
                    },
                    "turns":{
                        "taken":100000
                    }
                }
            }
        }

        super().__init__(resp)


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        shortid = request.form.get("shortid")
        if shortid=="testing":
            return render_template("index.html", playerdata = TestingPlayerData())
        data = gql("""{
    userByShortId(shortId: \""""+shortid+"""\") {
		name
		picture
		presence {
			status
			updatedAt
		}
		score
		stats {
			wins
			losses
            lifetimeTrophies
		}
        enhancedStats
	}
}""")
        print(data)
        result = client.execute(data)

        return render_template("index.html", playerdata = PlayerData(result))
    return render_template("index.html")



app.run()