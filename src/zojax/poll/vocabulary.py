from zope import interface
from zope.component import getUtility, getUtilitiesFor
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from interfaces import _, PUBLIC, VOTED_USERS, DONT_SHOW


class Vocabulary(SimpleVocabulary):

    def getTerm(self, value):
        try:
            return self.by_value[value]
        except KeyError:
            return self.by_value[self.by_value.keys()[0]]


def showResultsVocabulary(context):
    return SimpleVocabulary((
        SimpleTerm(PUBLIC, PUBLIC, _(u'Public')),
        SimpleTerm(VOTED_USERS, VOTED_USERS, _(u'Voted users')),
        SimpleTerm(DONT_SHOW, DONT_SHOW, _(u"Don't show")),
        ))


class PollsVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        configlet = getUtility(IPortalPollsConfiglet)

        terms = []
        for id, poll in configlet.registered.items():
            if IPortalPoll.providedBy(poll):
                terms.append((poll.configlet_title, id))
            else:
                terms.append(('Unknown', id))

        for name, poll in getUtilitiesFor(IPortalPoll):
            terms.append((poll.configlet_title, name))

        terms.sort()
        return Vocabulary([SimpleTerm(name,name,title)
                           for title, name in terms])
