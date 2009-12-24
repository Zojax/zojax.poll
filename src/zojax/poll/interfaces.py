from zope import interface, schema
from zope.i18nmessageid import MessageFactory

from zojax.content.type.interfaces import IItem
from zojax.richtext.field import RichText
from zojax.widget.list.field import SimpleList
from zojax.filefield.field import ImageField

from z3c.schema.baseurl.field import BaseURL

_ = MessageFactory('zojax.poll')

PUBLIC = 1
VOTED_USERS = 2
DONT_SHOW = 3


class IPollBase(IItem):

    enabled = schema.Bool(title=_(u'Poll enabled'),
                           description=u'',
                           default=True,
                           required=False)

    def getUID(self):

        ''' return IntId for Poll '''

    def hasVoted(self):

        ''' check, voted user(True) or not(False) '''

    def canVote(self):

        ''' check, can user vote(True) or not(False) '''

    def vote(self, values):

        ''' add user vote to poll history '''

    def clearResults(self):

        ''' cleanup poll voting history '''

    def getResults():

        ''' return list of results '''


class IPoll(IPollBase):
    ''' Simply poll '''

    text = RichText(title = _(u'Body text'),
                    required=False)

    logo = ImageField(title = _(u'Logo'),
                    required=False)

    showResults = schema.Choice(title=_(u'Show results'),
                                vocabulary='zojax.poll.showResults',
                                default=PUBLIC)

    def getResults():
        pass


class IPollDraft(interface.Interface):

    question  = schema.TextLine(
        title = _(u'Question'),
        description = _(u'Question text.'),
        default = u'',
        missing_value = u'',
        required = True)

    answers = SimpleList(
        title = _(u'Answers'),
        description = _(u'Poll answers'),
        required = True)

    allowCustom = schema.Bool(title=_(u'Enable custom choices'),
                               description=_(u"""Set it, if you want to allow
users to enter custom choices for this question (showing input box under predefined
choices)"""),
                               default=False,
                               required=False,
                               missing_value=True)

    numberOfChoices = schema.Int(
        title = _(u'Number of choices allowed'),
        default = 1,
        min = 1,
        required = True)


class IPollQuestion(IItem):

    title = schema.TextLine(
        title = _(u'Question'),
        description = _(u'Question text.'),
        default = u'',
        missing_value = u'',
        required = True)

    description = schema.TextLine(
        title = _(u'Description'),
        description = _(u'Question description.'),
        default = u'',
        missing_value = u'',
        required = False)

    allowCustom = schema.Bool(title=_(u'Enable custom choices'),
                               description=_(u"""Set it, if you want to allow
users to enter custom choices for this question (showing input box under predefined
choices)"""),
                               default=False,
                               required=False,
                               missing_value=True)

    numberOfChoices = schema.Int(
        title = _(u'Number of choices allowed'),
        default = 1,
        min = 1,
        required = True)


class IPollAnswer(IItem):
    """ poll answer """

    title = schema.TextLine(
        title = _(u'Answer'),
        description = _(u'Answer text.'),
        default = u'',
        missing_value = u'',
        required = True)



class IPollSet(IItem):
    """ Poll Set """

    text = RichText(title = _(u'Body text'),
                    required=False)

    firstPoll = interface.Attribute(_(u'First Poll'))

    lastPoll = interface.Attribute(_(u'Last Poll'))


class IVoteRecord(IItem):
    """ Vote record """

    choices = interface.Attribute(_(u'User choices'))


class IQuestionRecord(interface.Interface):
    """ Question record """

    voteCount = interface.Attribute(_(u'Vote count'))

    firstVote = interface.Attribute(_(u'First vote'))

    lastVote = interface.Attribute(_(u'Last vote'))


class IPollRecord(interface.Interface):
    """ Poll record """

    voteCount = interface.Attribute(_(u'Vote count'))

    firstVote = interface.Attribute(_(u'First vote'))

    lastVote = interface.Attribute(_(u'Last vote'))

    def getResults():
        pass

    def add(record):
        pass


class IPolling(interface.Interface):
    """ Polling utility """

    voteCount = interface.Attribute(_(u'Vote count'))

    def vote(self, poll_id, unicity_factor, choices):

        ''' save user votes '''

    def hasVoted(self, poll_id, unicity_factor):

        '''  '''
