
class GraphqlEndpoint {

  constructor(graphqlAddress) {
    this.graphqlAddress = graphqlAddress;
  }

  async fetchGraphql(query) {
    const eventFetch = await fetch(new Request(this.graphqlAddress), {
      method: 'POST',
      headers: {
        'Content-Type': 'text/plain',
        Accept: 'application/json',
      },
      body: `
        query {
          ${query}
        }
      `,
    });

    if (!eventFetch.ok) {
      throw new Error(`HTTP error! status: ${eventFetch.status}`);
    }
    
    return await eventFetch.json();
  }
}

export default GraphqlEndpoint;