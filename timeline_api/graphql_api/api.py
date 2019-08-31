from graphene import ObjectType, Schema, String, List, Field, ID

from graphql_api.model import Category, Group, Event

class Query(ObjectType):
    categories = Field(List(of_type=Category))

    groups = Field(List(of_type=Group))

    event = Field(Event, event_id=ID(required=True))

    events = Field(List(of_type=Event),
                   start_time=String(required=True),
                   end_time=String(required=True),
                   group_id=String(required=True))

    @staticmethod
    def resolve_categories(root, info):
        database = info.context.get('database')
        return database.get_categories()

    @staticmethod
    def resolve_groups(root, info):
        database = info.context.get('database')
        return database.get_groups()

    @staticmethod
    def resolve_event(root, info, event_id):
        database = info.context.get('database')
        return database.get_event(event_id)

    @staticmethod
    def resolve_events(root, info, start_time, end_time, group_id):
        database = info.context.get('database')
        return database.get_events(start=start_time, end=end_time, group_id=group_id)


schema = Schema(query=Query)
