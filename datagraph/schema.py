import graphene
import engine.schema


class Query(
        engine.schema.Query,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
