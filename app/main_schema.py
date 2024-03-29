import strawberry
from strawberry.fastapi import GraphQLRouter

from core.mutations import Mutation as CoreMutation
from core.queries import Query as CoreQuery


class Query(CoreQuery):
    pass


schema = strawberry.Schema(query=Query, mutation=CoreMutation)

graphql_app = GraphQLRouter(schema)
