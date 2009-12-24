from zope.interface import implements
from persistent import Persistent
from zope.component import getUtility
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.app.intid.interfaces import IIntIds
from zope.schema.fieldproperty import FieldProperty
from zope.location.interfaces import ILocation

from zojax.content.type.container import ContentContainer

from zojax.poll.interfaces import IPollQuestion


class PollQuestion(ContentContainer):
    implements(IPollQuestion)

    allowCustom = FieldProperty(IPollQuestion['allowCustom'])
    numberOfChoices = FieldProperty(IPollQuestion['numberOfChoices'])
