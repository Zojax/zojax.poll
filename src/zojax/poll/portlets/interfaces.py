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
from zope import schema

from zojax.portlets.contentitem.interfaces import  IContentItemPortlet

from zojax.poll.interfaces import _


class IPollPortlet(IContentItemPortlet):
    """ Portlet to show content of selected content item """

    item = schema.Choice(
        title = _(u'Poll Set'),
        description = _(u'Select content item.'),
        vocabulary = 'zojax.poll.portlet.poll.items',
        required = True)
