##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, component
from zope.security import checkPermission
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.app.intid.interfaces import IIntIds
from zope.traversing.api import getParents
from zope.traversing.interfaces import IContainmentRoot

from zojax.catalog.interfaces import ICatalog
from zojax.content.type.interfaces import IItem, IContent, IContentContainer
from zojax.portlets.contentitem import vocabulary

from interfaces import _


class PollItems(vocabulary.ContentItems):

    def __call__(self, context):
        catalog = component.queryUtility(ICatalog)
        ids = component.getUtility(IIntIds)

        if catalog is None:
            return Vocabulary(())

        terms = []
        for content in catalog.searchResults(type = {'any_of': ('content.pollset',)}):
            id = ids.getId(content)
            title = self.getTitle(content)
            terms.append((title, SimpleTerm(id, id, title)))

        terms.sort()
        return SimpleVocabulary([term for t, term in terms])
