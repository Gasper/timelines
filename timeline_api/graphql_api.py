from graphene import ObjectType, Schema, String, List, Field, ID

class Category(ObjectType):
    id = ID()
    name = String()

    @staticmethod
    def resolve_id(category, info):
        return category.get('id')
    
    @staticmethod
    def resolve_name(category, info):
        return category.get('name')

class Group(ObjectType):
    id = ID()
    name = String()
    category_id = String()

    @staticmethod
    def resolve_id(group, info):
        return group.get('id')
    
    @staticmethod
    def resolve_name(group, info):
        return group.get('name')
    
    @staticmethod
    def resolve_category_id(group, info):
        return group.get('category_id')

class Event(ObjectType):
    id = ID()
    start = String()
    end = String()
    title = String()
    description = String()
    group_id = String()

    @staticmethod
    def resolve_id(event, info):
        return event.get('id')

    @staticmethod
    def resolve_start(event, info):
        return event.get('start')

    @staticmethod
    def resolve_end(event, info):
        return event.get('end')

    @staticmethod
    def resolve_title(event, info):
        return event.get('title')

    @staticmethod
    def resolve_description(event, info):
        return event.get('description')
    
    @staticmethod
    def resolve_group_id(event, info):
        return event.get('group_id')

class Query(ObjectType):
    categories = Field(List(of_type=Category))

    groups = Field(List(of_type=Group))

    event = Field(Event, event_id=ID(required=True))

    events = Field(List(of_type=Event),
                   start_time=String(required=True),
                   end_time=String(required=True),
                   group=String(required=True))

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
    def resolve_events(root, info, start_time, end_time, group):
        database = info.context.get('database')
        return database.get_events(start=start_time, end=end_time, group=group)


schema = Schema(query=Query)
