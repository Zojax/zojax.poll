from persistent import Persistent
from zope.interface import implements
from zope import component
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.location.interfaces import ILocation
from zope.schema.fieldproperty import FieldProperty
from zope.app.intid.interfaces import IIntIdAddedEvent


from zojax.poll.interfaces import IVoteRecord


class VoteRecord(Persistent):
    implements(IVoteRecord)

    choices = {}

    def __init__(self, title, description='', choices=[]):
        self.choices = choices
        super(VoteRecord, self).__init__(title, description)


@component.adapter(IVoteRecord, IIntIdAddedEvent)
def recordIdAddedHandler(record, tevent):
    record.__parent__.add(record)
