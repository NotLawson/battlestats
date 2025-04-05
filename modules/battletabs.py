# Library for interacting with the battletabs GraphQL API
from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport
from gql.transport.requests import RequestsHTTPTransport

API = "https://battletabs.fly.dev/graphql"
WSAPI = "wss://battletabs.fly.dev/grapql "

class BattleTabsClient:
    def __init__(self, auth_token):
        headers = {
            "Authorization": "Bearer "+auth_token
        }
        self.transport = RequestsHTTPTransport(url=API, headers=headers, use_json=True)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)
    
    def raw_query(self, query):
        return self.client.execute_sync(gql("query {"+query+"}"))
    def raw_mutate(self, mutation):
        return self.client.execute_sync(gql("{mutate {"+mutation+"}"))

class UnAuthBattleTabsClient(BattleTabsClient):
    def __init__(self):
        self.transport = RequestsHTTPTransport(url=API, use_json=True)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)