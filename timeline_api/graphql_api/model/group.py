from graphene import ObjectType, String, ID

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