# Library for interacting with the battletabs GraphQL API
from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport
from gql.transport.requests import RequestsHTTPTransport


API = "wss://battletabs.fly.dev/graphql"

class BattleTabsClient:
    def __init__(self, auth_token):
        headers = {
            "Authorization": "Bearer "+auth_token
        }
        self.transport = RequestsHTTPTransport(url=API, headers=headers, use_json=True)
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
    
class BattleTabsClientUnAuth(BattleTabsClient):
    def __init__(self):
        self.transport = RequestsHTTPTransport(url=API, use_json=True)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)