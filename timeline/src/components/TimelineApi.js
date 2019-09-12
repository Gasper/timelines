/* eslint indent: "off" */

import Query from 'graphql-query-builder';
import { v4 as uuidv4 } from 'uuid';

class TimelineApi {
  constructor(graphqlEndpoint, cache) {
    this.graphqlEndpoint = graphqlEndpoint;
    this.cache = cache;
  }

  async fetchGraphql(query) {
    const eventFetch = await fetch(new Request(this.graphqlEndpoint), {
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

  async getGroupsAndCategories() {
    let categoriesQuery = new Query('categories');
    categoriesQuery.find('id', 'name');

    let groupsQuery = new Query('groups');
    groupsQuery.find(['id', 'name', 'categoryId']);

    let fullQuery = categoriesQuery.toString() + '\n' + groupsQuery.toString();

    return await this.fetchGraphql(fullQuery);
  }

  getMissingRangesQueries(groupIds, start, end) {

    let missingRangesQueries = new Map();

    for (const groupId of groupIds) {
      const missingRanges = this.cache.missingRanges(groupId, start, end);

      for (const missingRange of missingRanges) {

        let rangeQueryUuid = 'range' + uuidv4().replace(/-/g, '');

        let groupQuery = new Query('events', rangeQueryUuid);
        groupQuery.filter({
          startTime: missingRange.start,
          endTime: missingRange.end,
          groupId: groupId
        });
        groupQuery.find(['id', 'title', 'start', 'end', 'groupId']);

        missingRangesQueries.set(rangeQueryUuid, {
          queryString: groupQuery.toString(),
          groupId: groupId,
          start: missingRange.start,
          end: missingRange.end,
        });
      }
    }

    return missingRangesQueries;
  }

  async getEvents(groupIds, start, end) {

    let missingRangesQueries = this.getMissingRangesQueries(groupIds, start, end);

    if (missingRangesQueries.size > 0) {
      let missingRangesQueryStrings =
        Array.from(missingRangesQueries.values())
        .map(query => query.queryString);

      let fullQuery = missingRangesQueryStrings.join("\n");

      let missingData = await this.fetchGraphql(fullQuery);
      for (const [rangeUuid, rangeData] of missingRangesQueries) {
        this.cache.store(rangeData.groupId, rangeData.start, rangeData.end, missingData[rangeUuid]);
      }
    }

    var displayedEvents = [];
    for (const groupId of groupIds) {
      const storedEvents = this.cache.retrieve(groupId, start, end);
      displayedEvents = displayedEvents.concat(storedEvents);
    }

    return displayedEvents;
  }

  async getEvent(eventId) {

    let eventQuery = new Query('event');
    eventQuery.filter({eventId: eventId});
    eventQuery.find(['id', 'title', 'description']);

    let result = await this.fetchGraphql(eventQuery.toString());

    return result.event;
  }
}

export default TimelineApi;
