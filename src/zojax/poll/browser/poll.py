from zope.component import getUtility
from zope.app.security.principalregistry import UnauthenticatedPrincipal
from zope.app.intid.interfaces import IIntIds
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget, SequenceWidget
from zope.security.management import checkPermission
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL
from zope import component
from zope.interface import implements, Interface
from zope.session.interfaces import ISession
from zope.dublincore.interfaces import IDCTimes
from zope.security.interfaces import Unauthorized
from zope.security import checkPermission

from zojax.layoutform import form, button
from zojax.content.type.interfaces import IOrder
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.wizard.step import WizardStepForm

import time, random

from zojax.poll.interfaces import _, IPollBase, IPoll, IPollSet, IPollQuestion, \
                                  IPolling, PUBLIC, DONT_SHOW, VOTED_USERS

SESSION_SECTION = 'polling.session'


class PollView(form.PageletForm):

    def canVote(self):
        return checkPermission('zojax.poll.VotePoll', self.context) \
                and self.context.canVote(self.getVoteUnicity(create=0))

    def hasVoted(self):

        return self.context.hasVoted(self.getVoteUnicity(create=0))

    @button.buttonAndHandler(_(u'Vote >'), name='vote', condition=canVote)
    def vote(self, action):

        choices = []

        if self.canVote():
            votes = {}
            for name, question in self.context.items():
                choices = []
                id = self.ids.getId(removeSecurityProxy(question))
                for i in self.request.form.get('%s.answers.value'%id, []):
                    try:
                        if self.ids.queryObject(int(i)):
                            choices.append(int(i))
                    except (IndexError, KeyError, TypeError), e:
                        continue
                if question.allowCustom and self.request.form.get('%s.custom_answer'%id, ''):
                    choices.append(self.request.form['%s.custom_answer'%id])
                if not choices:
                    continue
                votes[id] = choices[:question.numberOfChoices]
            if votes:
                unicity = self.getVoteUnicity(create=1)
                self.context.vote(unicity, votes)

                IStatusMessage(self.request).add(_(u'Your vote saved, thank you!'))

            else:
                self.status = IStatusMessage(self.request).add(_(u'Please make choice'))

        else:
            self.status = IStatusMessage(self.request).add(_(u'You cannot vote on this poll'))

        return self.redirect(self.nextURL())

    def nextURL(self):
        return self.request.getURL()

    def getAnswers(self, question):
        return [{'answer': i, 'id': self.ids.getId(i)} for i in
                IOrder(removeSecurityProxy(question)).values()]

    def getResults(self):
        res = dict(self.context.getResults())
        for i in ['firstVote', 'lastVote']:
            vote = res[i]
            if vote is None:
                continue
            res[i] = IDCTimes(vote).created
        return res

    def getVoteUnicity(self, create = 1):

        """
        getVoteUnicity(self, poll_id, create = 1) => string or int or None

        return a tag that allows our poll to think that this vote isn't
        made twice for the same user.

        We first try to use the username as a tag. If it's not available or if
        the user is anonymous, we use a counter.

        - poll_id is the poll id (!), ie. a sitewide unique id identifying the poll.
          IT MUST NOT CHANGE DURING THE POLL'S LIFE.

        - create is an additional parameter set to 1 by default. If it is true,
          a new unicity token will be automatically generated. If it is false, this
          method returns the FORMER one if it exists, OR None if no token exists.
          This is convenient to check if a user has voted without consuming a
          ZODB transaction. => NOT USED
        """

        unicity = None

        poll_id = self.context.getUID()

        # Try to fetch the user name
        try:
            if not isinstance(self.request.principal, UnauthenticatedPrincipal):
                unicity = self.request.principal.id
        except:
            pass

        # If we didn't find a valid user name, then we use a counter and store it
        # in a cookie

        if not unicity:
            if self.request.has_key('AnonymousVoted%s' % (poll_id)):
                unicity = self.request['AnonymousVoted%s' % (poll_id)]
            elif create:
                unicity = int(time.time() * 10000000) + random.randint(0,99)
                expires = 'Wed, 26 Oct %s 10:00:00 GMT' % (time.localtime()[0]+10)
                self.request.response.setCookie(
                    'AnonymousVoted%s' % (poll_id,), str(unicity), path='/', expires=expires,
                    )

        # Add the poll id to the unicity factor
        if unicity:
            unicity = "%s%s" % (unicity, poll_id, )

        # Return unicity factor
        return unicity

    def update(self):
        self.ids = getUtility(IIntIds)
        self.questions = [{'question': i,
                           'id': self.ids.getId(removeSecurityProxy(i)),
                          'answers': self.getAnswers(i)}
                          for i in IOrder(self.context).values()]
        super(PollView, self).update()
        voted = self.hasVoted()
        self.showResultsLink = voted and self.context.showResults in [PUBLIC, VOTED_USERS] or \
                               self.context.showResults in [PUBLIC]
        self.showResults = self.showResultsLink


class PollResultsView(PollView):

    buttons = PollView.buttons.select()

    def update(self):
        super(PollResultsView, self).update()


class PollManagementView(WizardStepForm):

    label = _(u'Manage poll')

    @button.buttonAndHandler(_(u'Clear results'), name='clear')
    def clearResults(self, action):
        self.context.clearResults()
        self.status = IStatusMessage(self.request).add(_(u'Poll history is clean'))
        return self.redirect(self.request.getURL())
