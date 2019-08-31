from graphene import ObjectType, String, ID

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
