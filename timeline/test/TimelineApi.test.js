import TimelineApi from '../src/components/TimelineApi';
import SeriesCache from '../src/components/SeriesCache';

import 'jest';
import { v4 as uuidv4 } from 'uuid';
jest.mock('uuid');

function noWhitespace(inputString) {
  return inputString.replace(/\s/g, '');
}

test('groups and categories fetch builds a correct query', () => {
  let graphqlEndpointMock = {
    fetchGraphql: jest.fn(x => x),
  };

  let timelineApi = new TimelineApi(graphqlEndpointMock, {});
  timelineApi.getGroupsAndCategories();

  expect(graphqlEndpointMock.fetchGraphql.mock.calls.length).toBe(1);

  let query = noWhitespace(graphqlEndpointMock.fetchGraphql.mock.calls[0][0]);
  expect(query).toBe(noWhitespace(
    `
    categories {id, name}
    groups {id, name, categoryId}
    `
  ));
});

test('event fetch builds a correct query', () => {
  let graphqlEndpointMock = {
    fetchGraphql: jest.fn(x => x),
  };

  let timelineApi = new TimelineApi(graphqlEndpointMock, {});
  timelineApi.getEvent('event-4241');

  expect(graphqlEndpointMock.fetchGraphql.mock.calls.length).toBe(1);

  let query = noWhitespace(graphqlEndpointMock.fetchGraphql.mock.calls[0][0]);
  expect(query).toBe(noWhitespace(
    `
    event(eventId: "event-4241") {id, title, description}
    `
  ));
});

test('API is not queried if events are available in the cache', () => {
  let graphqlEndpointMock = {
    fetchGraphql: jest.fn(x => {}),
  };

  let seriesCache = new SeriesCache();
  seriesCache.store('series-A', '2020-03-01T00:00:00', '2020-03-19T00:00:00', []);

  let timelineApi = new TimelineApi(graphqlEndpointMock, seriesCache);
  timelineApi.getEvents(['series-A'], '2020-03-14T00:00:00', '2020-03-19T00:00:00');

  expect(graphqlEndpointMock.fetchGraphql.mock.calls.length).toBe(0);
});

test('events fetches all missing groups in one query', async () => {
  let graphqlEndpointMock = {
    fetchGraphql: jest.fn(x => {
      return {
        'range123456': [{id: '1234', start: '2020-03-16T00:00:00'}],
        'range153416': [],
        'range112233': [],  
      }
    }),
  };

  uuidv4
    .mockReturnValueOnce('12-34-56')
    .mockReturnValueOnce('15-34-16')
    .mockReturnValueOnce('11-22-33');

  let seriesCache = new SeriesCache();
  let timelineApi = new TimelineApi(graphqlEndpointMock, seriesCache);
  let events = await timelineApi.getEvents(['series-A', 'series-B', 'series-C'], '2020-03-14T00:00:00', '2020-03-19T00:00:00');

  expect(graphqlEndpointMock.fetchGraphql.mock.calls.length).toBe(1);
  expect(noWhitespace(graphqlEndpointMock.fetchGraphql.mock.calls[0][0]))
    .toBe(noWhitespace(
    `
    range123456: events (startTime: "2020-03-14T00:00:00", endTime: "2020-03-19T00:00:00", groupId: "series-A")  { id, title, start, end, groupId }
    range153416: events (startTime: "2020-03-14T00:00:00", endTime: "2020-03-19T00:00:00", groupId: "series-B")  { id, title, start, end, groupId }
    range112233: events (startTime: "2020-03-14T00:00:00", endTime: "2020-03-19T00:00:00", groupId: "series-C")  { id, title, start, end, groupId }
    `
  ));
  expect(events).toStrictEqual([{id: '1234', start: '2020-03-16T00:00:00'}]);
});
