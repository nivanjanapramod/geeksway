import graphene

import users.schema as UserSchema
import notes.schema as NoteSchema

class Query(UserSchema.Query, NoteSchema.Query, graphene.ObjectType):
    pass

class Mutation(UserSchema.Mutation, NoteSchema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)