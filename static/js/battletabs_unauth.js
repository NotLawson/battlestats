// BattleTabs Library for Client End

const client = graphqlWs.createClient({
    url: 'ws://localhost:8080/graphql',
    lazy: true,
    on: {
      connected: () => console.log('connected'),
      closed: () => console.log('closed'),
      error: (e) => console.error('error', e),
    }
  });