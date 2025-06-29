import strawberry
from strawberry.fastapi import GraphQLRouter

from .user_resolvers import UserQuery
from .transaction_resolvers import TransactionQuery

schema = strawberry.Schema(query=strawberry.type("Query", (UserQuery, TransactionQuery)))

graphql_app = GraphQLRouter(schema)
