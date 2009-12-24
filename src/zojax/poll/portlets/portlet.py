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
from zope import component, interface
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.traversing.api import getPath
from zope.security import checkPermission

from zojax.portlets.contentitem import portlet
from zojax.cache.view import cache
from zojax.cache.timekey import TagTimeKey, each20minutes
from zojax.content.space.portlets.cache import ContentTag
from zojax.portlet.cache import PortletModificationTag, PortletId

from zojax.portlet.portlet import PortletBase

from zojax.poll.cache import PollTag
from interfaces import IPollPortlet


def ViewAndContext(object, instance, *args, **kw):
    return {'context': getPath(instance.context),
            'content': instance.content is not None and getPath(instance.content) or '',
            'view': instance.view is not None and getPath(instance.view) or '',
            'principal': instance.request.principal.id,
            'request': 'form.buttons.vote' in instance.request and id(instance) or False}


class PollPortlet(portlet.ContentItemPortlet):
    """ Portlet to show content of selected content item """

    def update(self):
        super(PollPortlet, self).update()

    def isAvailable(self):
        return super(PollPortlet, self).isAvailable() \
               and checkPermission('zojax.poll.VotePoll', self.content)

    @cache(PortletId(),
           ViewAndContext, PortletModificationTag, ContentTag, PollTag)
    def updateAndRender(self):
        return PortletBase.updateAndRender(self)
