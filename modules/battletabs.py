# Library for interacting with the battletabs GraphQL API
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

API = "https://battletabs.fly.dev/graphql"
WSAPI = "wss://battletabs.fly.dev/grapql "

class BattleTabsClient:
    '''
    This allows us to connect to the BattleTabs API in a less messy way.
    '''
    def __init__(self, auth_token):
        headers = {
            "Authorization": "Bearer "+auth_token
        }
        self.transport = RequestsHTTPTransport(url=API, headers=headers, use_json=True)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)
    
    def raw_query(self, query):
        '''
        Sends a query to the BattleTabs API
        '''
        return self.client.execute_sync(gql("query {"+query+"}"))
    def raw_mutate(self, mutation):
        '''
        Sends a mutation to the BattleTabs API
        '''
        return self.client.execute_sync(gql("{mutate {"+mutation+"}"))

class UnAuthBattleTabsClient(BattleTabsClient):
    '''
    This allows us to connect without auth to the BattleTabs API in a less messy way.
    '''
    def __init__(self):
        self.transport = RequestsHTTPTransport(url=API, use_json=True)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)