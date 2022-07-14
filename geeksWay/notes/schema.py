from datetime import datetime
import graphene
from graphene_django import DjangoObjectType

from .models import Notes

class NoteType(DjangoObjectType):
    class Meta:
        model = Notes


class Query(graphene.ObjectType):
    all_notes = graphene.List(NoteType, id=graphene.ID())
    notes = graphene.Field(NoteType, id=graphene.ID())

    def resolve_all_notes(self, info, **kwargs):
        return Notes.objects.filter(user=info.context.user)

    def resolve_notes(self, info, id):
        return Notes.objects.get(pk=id)


#mutations

class CreateNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        created_on = graphene.DateTime()
        last_updated = graphene.DateTime()
        description = graphene.String()

    note = graphene.Field(NoteType)

    def mutate(self, info, title=None, description=None, created_on=None, last_updated=None):
        note = Notes.objects.create(user = info.context.user, title=title, description=description, created_on=datetime.now(), last_updated=datetime.now())
        note.save()
        return CreateNote(
            note=note
        )


class UpdateNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        created_on = graphene.DateTime()
        last_updated = graphene.DateTime()
        description = graphene.String()
    
    note = graphene.Field(NoteType)

    def mutate(self, info, id, title=None, description=None):
        note = Notes.objects.get(pk=id)
        note.title = title if title is not None else note.title
        note.last_updated = datetime.now()
        note.description = description if description is not None else note.description
    
        note.save()
        return UpdateNote(
            note=note
        )


class DeleteNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        created_on = graphene.DateTime()
        last_updated = graphene.DateTime()
        description = graphene.String()

    note = graphene.Field(NoteType)

    def mutate(seld, info, id):
        note = Notes.objects.get(pk=id)

        if note is not None:
            note.delete()
            return DeleteNote(note=note)


class Mutation(graphene.ObjectType):
  create_note = CreateNote.Field()
  update_note = UpdateNote.Field()
  delete_note = DeleteNote.Field()