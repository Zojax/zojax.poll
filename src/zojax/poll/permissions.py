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
from zope.component import queryAdapter
from zojax.content.space.interfaces import ISpace
from zojax.content.permissions.permission import ContentPermission


@component.adapter(ISpace, interface.Interface)
def forumPermissionContentTypes(context, permissions):
    if ('zojax.poll.AddQuestion' in permissions or
        'zojax.poll.SubmitQuestion' in permissions or
        'zojax.poll.AddPoll' in permissions or
        'zojax.poll.SubmitPoll' in permissions):
        return 'content.pollset', 'content.poll'
