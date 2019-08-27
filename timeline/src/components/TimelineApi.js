/* eslint indent: "off" */

class TimelineApi {
  constructor(graphqlEndpoint) {
    this.graphqlEndpoint = graphqlEndpoint;
  }

  async fetchGraphql(query) {
    const eventFetch = await fetch(new Request(this.graphqlEndpoint), {
      method: 'POST',
      headers: {
        'Content-Type': 'text/plain',
        Accept: 'application/json',
      },
      body: query,
    });

    if (!eventFetch.ok) {
      throw new Error(`HTTP error! status: ${eventFetch.status}`);
    }
    
    return await eventFetch.json();
  }

  async getGroups() {
    const queryResult = await this.fetchGraphql(`
      query {
        categories {id, name}
        groups {id, name, categoryId}
      }`);

    return queryResult;
  }

  async getEvents(groupId, startDateTime, endDateTime) {
    const queryResult = await this.fetchGraphql(`
      query {
        events(startTime: "${startDateTime}", endTime: "${endDateTime}",
        groupId: "${groupId}") {
          id, title, description,
          start, end,
          groupId
      }
    }`);

    return queryResult.events;
  }
}

export default TimelineApi;
