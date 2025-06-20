// BattleTabs Library for Client End

const client = graphqlWs.createClient({
    url: 'ws://localhost:8080/graphql',
    connectionParams: () => {
        return {
        authToken: document.getElementById('authToken').value,
      };
    },
    lazy: true,
    on: {
      connected: () => console.log('connected'),
      closed: () => console.log('closed'),
      error: (e) => console.error('error', e),
    },
    onConnected: () => {
      console.log('Connected to GraphQL WebSocket server');
      client.subscribe({ query: 'subscription { battleTabs { id name } }' }, {
        next: (data) => {
          console.log('Received data:', data);
          updateBattleTabs(data.data.battleTabs);
        },
        error: (error) => {
          console.error('Error in subscription:', error);
        },
      });
    }
  });