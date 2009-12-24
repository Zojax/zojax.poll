from zope.interface import implements
from persistent import Persistent
from BTrees.Length import Length
from zope.component import getUtility, adapts
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.app.intid.interfaces import IIntIds
from zope.schema.fieldproperty import FieldProperty
from zope.location.interfaces import ILocation
from zope.app.container.contained import NameChooser
from zope.security.proxy import removeSecurityProxy
from zope.cachedescriptors.property import Lazy
from zope.exceptions import UserError

from zojax.richtext.field import RichTextProperty
from zojax.content.type.container import ContentContainer

from interfaces import _, IPollSet, IPolling


class PollSet(ContentContainer):

    implements(IPollSet)

    text = RichTextProperty(IPollSet['text'])

    def getResults(self):

        res=getUtility(IPolling).getResults(self.getUID())
        return
        #[[{'question': u'test', 'choices': [u'1']},
        #  {'question': u'test2', 'choices': [u'3']},
        #  {'question': u'test23', 'choices': [u'12']}]]
        results = {}
        for ur in res:
            for q in ur:
                for c in q['choices']:
                    if results.has_key(q['question']):
                        results[q['question']].append()
                    else:
                        results[q['question']][c] = {'title' : c,
                                                     'votes' : 1,
                                                     'persents' : 0}

        asum=float(sum([res[k]['count'] for k in res]))

        wrapped=[]

        for k in res.keys():
            wrapped.append({'title' : k,
                            'votes' : res[k]['count'],
                            'percents' : '%.2f' % (float(res[k]['count'])/asum*100.)})

        return wrapped

    @Lazy
    def _next_id(self):
        next = Length(1)
        self._p_changed = True
        return next

    @property
    def nextId(self):
        id = self._next_id()
        self._next_id.change(1)
        return u'%0.5d'%id

    @property
    def lastPoll(self):
        try:
            return self[self._SampleContainer__data.maxKey()]
        except ValueError:
            return None

    @property
    def firstPoll(self):
        try:
            return self[self._SampleContainer__data.minKey()]
        except ValueError:
            return None

    def __delitem__(self, key):
        if len(self) == 1:
            raise UserError(_(u"Can't delete last poll in set"))
        super(PollSet, self).__delitem__(key)


class PollSetNameChooser(NameChooser):
    adapts(IPollSet)

    def __init__(self, context):
        self.context = context

    def chooseName(self, name, object):
        return removeSecurityProxy(self.context).nextId
