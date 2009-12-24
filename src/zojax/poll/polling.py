from rwproperty import getproperty, setproperty

from BTrees.Length import Length

from zope import interface
from zope.app.container.interfaces import IContainer
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent

from zojax.content.type.configlet import ContentContainerConfiglet

from interfaces import IPolling
from voterecord import VoteRecord
from pollrecord import PollRecord


class Polling(ContentContainerConfiglet):
    interface.implements(IPolling)

    @getproperty
    def voteCount(self):
        res = getattr(self.data, 'voteCount', None)
        if res is None:
            res = Length()
            self.data.voteCount = res
        return res

    def vote(self, poll_id, unicity_factor, choices):
        poll_id = str(poll_id)#type of id - str

        if not self.has_key(poll_id):
            record = PollRecord()
            notify(ObjectCreatedEvent(record))
            self[poll_id] = record
        voterecord = VoteRecord(poll_id, choices=choices)
        notify(ObjectCreatedEvent(voterecord))
        self[poll_id][unicity_factor] = voterecord

    def hasVoted(self, poll_id, unicity_factor):

        return self.get(str(poll_id), {}).has_key(unicity_factor)

    def clearResults(self, poll_id):

        try:
            del self[str(poll_id)]
        except KeyError:#not results also
            pass

    def getResults(self, poll_id):

        poll_id = str(poll_id)
        if poll_id not in self:
            return {}, None
        return self[poll_id].getResults()
