from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport

API = "wss://battletabs.fly.dev/graphql"


# Select your transport with a defined url endpoint
transport = WebsocketsTransport(url=API, init_payload={
        "authToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI5YmM3YzdlNy0xY2ViLTQ4YjAtYTAwMC0xOTI4Y2I2MTU0ZTgiLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTczMDY5Mjk4OCwiZXhwIjoxNzMxMjk3Nzg4fQ.t4FExu5pd44SaTQxuXdvSVUwbA83wkm-93lCe_0UjBI",
        "client-version": "55.3.0.3965",
        "platform": "web",
        "platformSubKind": "web",
        "iframeParent": "https://battletabs.io",
        "deviceId": "21498e65-d9a8-4663-a94c-2d6b939eeb51"
    })

client = Client(transport=transport, fetch_schema_from_transport=True)



query = gql(
"""
subscription {
	battleCreated {
		id
		players {
			name
		}
	}
}
"""
)


print("Battles:")

for result in client.subscribe(query):
	print(result)

