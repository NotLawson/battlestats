from flask import Flask, render_template, request
from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport
import json, os
from datetime import datetime
import mysql.connector
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

influx_token = os.environ.get("INFLUXDB_TOKEN")

org = "battlestats"
url = "http://influx:8086"
influx_client = influxdb_client.InfluxDBClient(url=url, token=influx_token, org=org)
influx_write = influx_client.write_api(write_options=SYNCHRONOUS)
influx_get = influx_client.query_api()

class Database:
    def __init__(self, database):
        self.connector = mysql.connector.connect(
            host="db",
            user="root",
            password="battlestats",
            database="database"
        )
    def query(self, query):
        cursor = self.connector.cursor()
        cursor.execute(query)
        return cursor
    
    def close(self):
        self.connector.disconnect()


def save_playerdata(playerdata):
    influx_write.write("winrate", "battlestats", Point("winrate").tag("shortid", playerdata.shortid).field("value", playerdata.wr))
    influx_write.write("winstreak", "battlestats", Point("winstreak").tag("shortid", playerdata.shortid).field("value", playerdata.current_winstreak))
    influx_write.write("trophies", "battlestats", Point("trophies").tag("shortid", playerdata.shortid).field("value", playerdata.trophies))




app = Flask(__name__)
API = "https://battletabs.fly.dev/graphql"


# Select your transport with a defined url endpoint
transport = WebsocketsTransport(url=API, init_payload={
        "authToken": "auth token placeholder, need a way to gen one",
        "client-version": "55.3.0.3965",
        "platform": "web",
        "platformSubKind": "web",
        "iframeParent": "https://battletabs.io",
        "deviceId": "21498e65-d9a8-4663-a94c-2d6b939eeb51"
    })

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

class PlayerData:
    def __init__(self, resp):
        #self.json = json.loads(resp)
        self.json = resp
        self.shortid = self.json["userByShortId"]["shortId"]
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
                },
                "shortId":"testing"
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
        shortId
	}
}""")
        print(data)
        result = client.execute(data)
        playerdata = PlayerData(result)
        save_playerdata(playerdata)

        return render_template("index.html", playerdata = playerdata)
    return render_template("index.html")

@app.route("/api/<item>/<shortid>")
def api(item, shortid):
    table = influx_get.query(f"""
from(bucket: "{item}")
    |> filter(fn: r => r.shortid == "{shortid}")
""")
    out = table.to_values(["_time", "value"])
    x = []
    y = []
    for row in out:
        x.append(row[0].strftime("%Y-%m-%dT%H:%M:%SZ"))
        y.append(int(row[1]))
    return {
        "shortid":shortid,
        "x":x,
        "y":y
    }


app.run()



