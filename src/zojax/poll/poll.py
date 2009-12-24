from zope.interface import implements, alsoProvides
from persistent import Persistent
from zope.component import getUtility, adapter
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.app.intid.interfaces import IIntIds
from zope.schema.fieldproperty import FieldProperty
from zope.location.interfaces import ILocation
from zope.lifecycleevent import ObjectCreatedEvent
from zope.event import notify

from zojax.filefield.field import FileFieldProperty
from zojax.richtext.field import RichTextProperty
from zojax.content.draft.interfaces import IDraftPublishedEvent
from zojax.content.type.container import ContentContainer
from zojax.content.type.interfaces import IUnremoveableContent, IContentType
from zojax.content.type.interfaces import IDraftedContent, IOrder
from zojax.content.draft.draft import DraftContent

from interfaces import IPoll, IPolling, IPollDraft
from question import PollQuestion
from answer import PollAnswer


class BasePoll(object):

    enabled = FieldProperty(IPoll['enabled'])

    def getUID(self):

        return getUtility(IIntIds).getId(self)

    def hasVoted(self, unicity):

        polling = getUtility(IPolling)

        uid = self.getUID()

        return polling.hasVoted(uid, unicity)

    def canVote(self, unicity):

        can_vote = False

        if self.enabled and not self.hasVoted(unicity):
            can_vote = True

        return can_vote

    def vote(self, unicity_factor, choices):

        uid = self.getUID()

        polling = getUtility(IPolling)

        polling.vote(uid, unicity_factor, choices)

    def clearResults(self):

        getUtility(IPolling).clearResults(self.getUID())


class Poll(BasePoll, ContentContainer):

    implements(IPoll)

    text = RichTextProperty(IPoll['text'])

    logo = RichTextProperty(IPoll['logo'])

    def getResults(self):
        res = []
        ids = getUtility(IIntIds)
        results, record = getUtility(IPolling).getResults(self.getUID())
        if not results:
            return {'results':{},
                    'voteCount': 0,
                    'firstVote': None,
                    'lastVote': None}
        for question in IOrder(self).values():
            id = ids.getId(question)
            value = results.get(id)
            if value is None:
                continue
            answers = []
            items = []

            for answer in IOrder(question).values():
                id = ids.getId(answer)
                if id in value:
                    items.append((id, value.pop(id)))

            for answer_id, answer_data in (items + value.items()):
                try:
                    answer = ids.queryObject(answer_id)
                except TypeError:
                    answer = None
                if answer is None:
                    answers.append({'title': answer_id,
                                    'results':  answer_data})
                else:
                    answers.append({'title': answer.title,
                                    'results':  answer_data})
            res.append({'question': question,
                        'answers': answers
                        })
        return {'results':res,
                'voteCount': record.voteCount.value,
                'firstVote': record.firstVote,
                'lastVote': record.lastVote}


class PollDraft(DraftContent):
    implements(IPollDraft)

    def publish(self, comment=u''):
        content = super(PollDraft, self).publish(comment)

        question = PollQuestion(self.question)
        notify(ObjectCreatedEvent(question))
        question.allowCustom = self.allowCustom
        question.numberOfChoices = self.numberOfChoices
        IContentType(content).add(question)

        for i in self.answers:
            answer = PollAnswer(i)
            notify(ObjectCreatedEvent(answer))
            IContentType(question).add(answer)
        return content
