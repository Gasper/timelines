import sys
sys.path.append('..')

import unittest
import graphql_api

class ApiTest(unittest.TestCase):

  def test_get_categories(self):
    """
    Tests fetching all fileds of the categories.
    """
    class MockDb:
      def get_categories(self):
        return [
          {'id': '123', 'name': 'Category 1'},
          {'id': '456', 'name': 'Category 2'},
          {'id': '678', 'name': 'Category 3'},
        ]
    
    db = MockDb()
    query = "query { categories {id, name} }"

    result = graphql_api.schema.execute(query, context_value={'database': db})
    self.assertDictEqual(result.data, {
      'categories': [
        {'id': '123', 'name': 'Category 1'},
        {'id': '456', 'name': 'Category 2'},
        {'id': '678', 'name': 'Category 3'},
      ]}
    )
    
  def test_get_groups(self):
    """
    Tests fetching all fields of the groups.
    """
    class MockDb:
      def get_groups(self):
        return [
          {'id': '111', 'name': 'Group 1', 'category_id': '123'},
          {'id': '433', 'name': 'Group 2', 'category_id': '123'},
          {'id': '151', 'name': 'Group 3', 'category_id': '456'},
        ]
    
    db = MockDb()
    query = "query { groups {id, name, categoryId} }"

    result = graphql_api.schema.execute(query, context_value={'database': db})
    self.assertDictEqual(result.data, {
      'groups': [
        {'id': '111', 'name': 'Group 1', 'categoryId': '123'},
        {'id': '433', 'name': 'Group 2', 'categoryId': '123'},
        {'id': '151', 'name': 'Group 3', 'categoryId': '456'},
      ]}
    )
  
  def test_get_event(self):
    """
    Tests fetching all fields and description of the specific event.
    """
    class MockDb:
      def get_event(self, event_id):
        return {'id': event_id, 'start': '2020-09-07', 'end': '2020-10-08',
          'title': 'Event 7', 'description': 'Evt dscr', 'group_id': '123'}
    
    db = MockDb()
    full_query = 'query { event(eventId: "6543") {id, start, end, title, description, groupId} }'

    result = graphql_api.schema.execute(full_query, context_value={'database': db})
    self.assertDictEqual(result.data, {
      'event': {
          'id': '6543', 'start': '2020-09-07', 'end': '2020-10-08',
          'title': 'Event 7', 'description': 'Evt dscr', 'groupId': '123'
        }
      }
    )

    description_query = 'query { event(eventId: "223") {id, description} }'

    result = graphql_api.schema.execute(description_query, context_value={'database': db})
    self.assertDictEqual(result.data, {
      'event': { 'id': '223', 'description': 'Evt dscr'}
      }
    )
  
  def test_get_events(self):
    """
    Tests fetching events for a specific group and time range.
    """
    class MockDb:
      def get_events(self, start, end, group_id):
        return [
          {'id': 'ev0', 'start': start, 'end': end,
          'title': 'Event 08', 'description': 'Evt dscr0', 'group_id': group_id},
          {'id': 'ev1', 'start': start, 'end': end,
          'title': 'Event 18', 'description': 'Evt dscr1', 'group_id': group_id},
          {'id': 'ev2', 'start': start, 'end': end,
          'title': 'Event 28', 'description': 'Evt dscr2', 'group_id': group_id}
        ]
    
    db = MockDb()
    full_query = """
    query { 
      events(startTime: "2020-12-12", endTime: "2020-12-15", groupId: "8") {
        id, start, end, title, description, groupId
      } 
    }
    """

    result = graphql_api.schema.execute(full_query, context_value={'database': db})
    self.assertDictEqual(result.data, {
        'events': [
          {'id': 'ev0', 'start': '2020-12-12', 'end': '2020-12-15',
          'title': 'Event 08', 'description': 'Evt dscr0', 'groupId': '8'},
          {'id': 'ev1', 'start': '2020-12-12', 'end': '2020-12-15',
          'title': 'Event 18', 'description': 'Evt dscr1', 'groupId': '8'},
          {'id': 'ev2', 'start': '2020-12-12', 'end': '2020-12-15',
          'title': 'Event 28', 'description': 'Evt dscr2', 'groupId': '8'}
        ]
      }
    )

  def test_get_events_mandatory_start(self):
    """
    Tests that missing start time signals an error when fetching events for a group.
    """
    class MockDb:
      def get_events(self, start, end, group_id):
        return [
          {'id': 'ev0', 'start': start, 'end': end,
          'title': 'Event 08', 'description': 'Evt dscr0', 'group_id': group_id}
        ]
    
    db = MockDb()
    query_no_start = """
    query { 
      events(endTime: "2020-12-15", groupId: "8") {
        id, start, end, title, description, groupId
      } 
    }
    """

    result = graphql_api.schema.execute(query_no_start, context_value={'database': db})
    self.assertTrue(result.errors)

  def test_get_events_mandatory_end(self):
    """
    Tests that missing end time signals an error when fetching events for a group.
    """
    class MockDb:
      def get_events(self, start, end, group_id):
        return [
          {'id': 'ev0', 'start': start, 'end': end,
          'title': 'Event 08', 'description': 'Evt dscr0', 'group_id': group_id}
        ]
    
    db = MockDb()
    query_no_end = """
    query { 
      events(startTime: "2020-12-11", groupId: "8") {
        id, start, end, title, description, groupId
      } 
    }
    """

    result = graphql_api.schema.execute(query_no_end, context_value={'database': db})
    self.assertTrue(result.errors)

  def test_get_events_mandatory_group(self):
    """
    Tests that missing group ID signals an error when fetching events for a group.
    """
    class MockDb:
      def get_events(self, start, end, group_id):
        return [
          {'id': 'ev0', 'start': start, 'end': end,
          'title': 'Event 08', 'description': 'Evt dscr0', 'group_id': group_id}
        ]
    
    db = MockDb()
    query_no_group = """
    query { 
      events(startTime: "2020-12-11", endTime: "2020-12-19") {
        id, start, end, title, description, groupId
      } 
    }
    """

    result = graphql_api.schema.execute(query_no_group, context_value={'database': db})
    self.assertTrue(result.errors)

  def test_get_event_mandatory_id(self):
    """
    Tests that missing event ID signals an error when fetching specific event.
    """
    class MockDb:
      def get_event(self, event_id):
        return {'id': event_id, 'start': '2020-12-03', 'end': '2020-13-18',
          'title': 'Event 33', 'description': '', 'group_id': '345'}
    
    db = MockDb()
    no_id_query = 'query { event {id, start, end, title, description, groupId} }'

    result = graphql_api.schema.execute(no_id_query, context_value={'database': db})
    self.assertTrue(result.errors)

if __name__ == '__main__':
  unittest.main()
