import pymongo


class MongoDatabase:
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.collection = client.events.events

    def get_events(self, start, end, group_id):
        query = {
            'start': {'$lt': end},
            'end': {'$gt': start},
            'group_id': {'$eq': group_id},
        }
        return self.collection.find(query)

    def get_event(self, event_id):
        return self.collection.find_one({'id': event_id})
