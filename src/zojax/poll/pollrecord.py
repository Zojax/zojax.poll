from persistent import Persistent
from BTrees.OOBTree import OOBTree
from BTrees.Length import Length
from zope.interface import implements
from zope.component import getUtility
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.location.interfaces import ILocation
from zope.schema.fieldproperty import FieldProperty
from zope.cachedescriptors.property import Lazy
from zope.app.container.btree import BTreeContainer
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent


from zojax.content.type.interfaces import IContentContainer
from zojax.poll.interfaces import IPollRecord, IQuestionRecord, IPolling
from cache import PollTag

class QuestionRecord(Persistent):

    implements(IQuestionRecord)

    voteCount = None

    firstVote = None

    lastVote = None

    def __init__(self):
        self._tree = OOBTree()
        self.voteCount = Length()

    def __contains__(self, key):
        '''See interface IReadContainer

        >>> c = BTreeContainer()
        >>> "a" in c
        False
        >>> c["a"] = 1
        >>> "a" in c
        True
        >>> "A" in c
        False
        '''
        return key in self._tree

    @Lazy
    def _QuestionRecord__len(self):
        l=Length()
        ol = len(self._tree)
        if ol>0:
            l.change(ol)
        self._p_changed=True
        return l

    def __len__(self):
        return self.__len()

    def _setitemf(self, key, value):
        # make sure our lazy property gets set
        l = self.__len
        self._tree[key] = value
        l.change(1)

    def __iter__(self):
        return iter(self._tree)

    def __getitem__(self, key):
        '''See interface `IReadContainer`'''
        return self._tree[key]

    def get(self, key, default=None):
        '''See interface `IReadContainer`'''
        return self._tree.get(key, default)

    def __setitem__(self, key, value):
        self._setitemf(key, value)

    def __delitem__(self, key):
        # make sure our lazy property gets set
        l = self.__len
        del self._tree[key]
        l.change(-1)

    has_key = __contains__

    def items(self):
        '''See interface `IReadContainer`'''
        return self._tree.items()

    def keys(self):
        '''See interface `IReadContainer`'''
        return self._tree.keys()

    def values(self):
        '''See interface `IReadContainer`'''
        return self._tree.values()


class PollRecord(BTreeContainer):
    implements(IPollRecord, IContentContainer)

    voteCount = None

    firstVote = None

    lastVote = None

    def __init__(self, *kv, **kw):
        super(PollRecord, self).__init__(*kv, **kw)
        self._results = OOBTree()
        self.voteCount = Length()

    def add(self, record):
        polling = getUtility(IPolling)
        for key, value in record.choices.items():
            item = self._results.get(key)
            if item is None:
                item = QuestionRecord()
                notify(ObjectCreatedEvent(item))
                self._results[key] = item
            for id in value:
                self.voteCount.change(1)
                polling.voteCount.change(1)
                item.voteCount.change(1)
                if item.firstVote is None:
                    item.firstVote = record
                item.lastVote = record
                answer = item.get(id)
                if answer:
                    answer.change(1)
                else:
                    item[id] = Length(1)
        if self.firstVote is None:
            self.firstVote = record
        self.lastVote = record
        self._p_changed = 1

    def getResults(self):
        res = {}
        for question, answers in self._results.items():
            res[question] = {}
            size = float(answers.voteCount.value)
            for answer, votes in answers.items():
                res[question][answer] = (votes.value, votes.value/size)
        return res, self


def pollRecordHandler(record, ev):
    PollTag.update(record)
