import pymongo
import argparse

from demo_db import generate_categories, generate_groups, generate_events

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Populate MongoDB database with events')
    parser.add_argument('--host', default='localhost', help='IP/Host of the mongoDB database')
    parser.add_argument('--port', default=27017, help='Port of the mongoDB database')
    args = parser.parse_args()

    client = pymongo.MongoClient(args.host, args.port)
    categories_collection = client.timeline.categories
    groups_collection = client.timeline.groups
    events_collection = client.timeline.events

    for category in generate_categories():
        categories_collection.insert_one(category)
        print(category)

    for group in generate_groups():
        groups_collection.insert_one(group)
        print(group)

    for event in generate_events():
        events_collection.insert_one(event)
        print(event)
