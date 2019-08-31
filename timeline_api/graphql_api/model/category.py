from graphene import ObjectType, String, ID

class Category(ObjectType):
    id = ID()
    name = String()

    @staticmethod
    def resolve_id(category, info):
        return category.get('id')
    
    @staticmethod
    def resolve_name(category, info):
        return category.get('name')