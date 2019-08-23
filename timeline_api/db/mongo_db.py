import pymongo


class MongoDatabase:
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.categories_collection = client.timeline.categories
        self.groups_collection = client.timeline.groups
        self.events_collection = client.timeline.events
    
    def get_categories(self):
        return self.categories_collection.find()
    
    def get_groups(self):
        return self.groups_collection.find()

    def get_events(self, start, end, group_id):
        query = {
            'start': {'$lt': end},
            'end': {'$gt': start},
            'group_id': {'$eq': group_id},
        }
        return self.events_collection.find(query)

    def get_event(self, event_id):
        return self.events_collection.find_one({'id': event_id})
