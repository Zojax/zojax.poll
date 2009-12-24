from zope import interface
from zope.component import getUtility

from interfaces import IPortalPoll, IBoundPortalPoll, IPortalPollsConfiglet


class PortalPoll(object):

    id = None

    def __bind__(self, context, request):
        clone = self.__class__.__new__(self.__class__)
        clone.__dict__.update(self.__dict__)
        clone.context = context
        clone.request = request
        interface.directlyProvides(clone, IBoundPortalPoll)
        return clone

    def isAvailable(self):
        return IBoundPortalPoll.providedBy(self)

    def getSubmenu(self):
        if not IBoundPortalPoll.providedBy(self):
            return ()

        configlet = getUtility(IPortalPollsConfiglet)

        polls = []
        for pollId in self.submenu:
            poll = configlet.getPoll(pollId)
            if IPortalPoll.providedBy(poll):
                poll = poll.__bind__(self.context, self.request)
                if poll.isAvailable():
                    polls.append(poll)
        return polls
