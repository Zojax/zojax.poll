import random
from BTrees.OOBTree import OOBTree

from zope import interface, component
from zope.component import queryUtility, getUtilitiesFor
from zope.location import LocationProxy
from zope.publisher.interfaces import NotFound
from z3c.traverser.interfaces import ITraverserPlugin

from interfaces import IPortalPoll, IPortalPollsConfiglet


class PortalPollsConfiglet(object):
    interface.implements(IPortalPollsConfiglet)

    @property
    def registered(self):
        data = self.data.get('registered')
        if data is None:
            data = OOBTree()
            self.data['registered'] = data

        return data

    def getPoll(self, pollId):
        poll = self.registered.get(pollId)
        if poll is None:
            poll = queryUtility(IPortalPoll, pollId)

        return poll

    def getPolls(self, context, request):
        polls = []
        for pollId in self.polls:
            poll = self.getPoll(pollId)
            if IPortalPoll.providedBy(poll):
                poll = poll.__bind__(context, request)
                if poll.isAvailable():
                    polls.append(poll)
        return polls

    def registerPoll(self, poll):
        registered = self.registered

        if poll.id:
            id = poll.id
        else:
            id = random.randint(1, 10000)
            while id in registered:
                id += 1

            poll.id = id

        self.registered[id] = poll

        if id not in self.polls:
            self.polls.append(id)
            self.polls = self.polls

    def unregisterPoll(self, id):
        if id in self.registered:
            del self.registered[id]

            if id in self.polls:
                self.polls.remove(id)
                self.polls = self.polls


class TraverserPlugin(object):
    interface.implements(ITraverserPlugin)
    component.adapts(IPortalPollsConfiglet, interface.Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        try:
            id = int(name)
        except:
            raise NotFound(self.context, name, request)

        poll = self.context.registered.get(id)
        if poll is None:
            raise NotFound(self.context, name, request)

        return LocationProxy(poll, self.context, name)
