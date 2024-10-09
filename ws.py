from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport
from gql.transport.aiohttp import AIOHTTPTransport

import asyncio

#API = "wss://battletabs.fly.dev/graphql"
API = "https://battletabs.fly.dev/graphql"

#client = Client(transport=WebsocketsTransport(url=API), fetch_schema_from_transport=True)

transport = WebsocketsTransport(url=API, init_payload={
        "authToken": "[redacted, i'll make a sercrets file at some point]",
        "client-version": "55.3.0.3965",
        "platform": "web",
        "platformSubKind": "web",
        "iframeParent": "https://battletabs.io",
        "deviceId": "21498e65-d9a8-4663-a94c-2d6b939eeb51"
    })



print(transport.init_payload)
client = Client(transport=AIOHTTPTransport(url=API), fetch_schema_from_transport=True)

shortid = "ZpJd876xK"
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

actions = gql("{\nactiveBattles {\nid\n}\n}")


print(client.execute(actions))


