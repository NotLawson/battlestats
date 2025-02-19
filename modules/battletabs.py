# Library for interacting with the battletabs GraphQL API
from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport
as

API = "wss://battletabs.fly.dev/graphql"

class BattleTabsClient:
    def __init__(self, auth_token):
        init_payload = {
            "authToken": auth_token,
            "client-version": "55.3.0.3965",
            "platform": "web",
            "platformSubKind": "web",
            "iframeParent": "https://battletabs.io",
            "deviceId": "21498e65-d9a8-4663-a94c-2d6b939eeb51"
        }
        self.transport = WebsocketsTransport(url=API, init_payload=init_payload)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)
    
    def query(self, query):
        return self.client.execute_sync(gql(query))
    def mutate(self, mutation):
        return self.client.execute_sync(gql(mutation))
    
    def get_user(self, user):
        query = """{
user(username: '"""+user+"""') {
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
	}} """
        return self.query(query)


class SelfDestructClient(BattleTabsClient):
    async def query(self, query):
        q = super().query(query)
        await self.transport.close()
        return q