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
from zope import interface, component, schema
from zope.exceptions.interfaces import UserError
from zope.app.container.interfaces import \
    IWriteContainer, IContainerNamesContainer, INameChooser

from z3c.form import validator
from z3c.form.error import ErrorViewSnippet

from zojax.layoutform import button, Fields, PageletEditSubForm
from zojax.content.draft.interfaces import IDraftedContent

from zojax.poll.interfaces import IPollDraft


class PollDraftForm(PageletEditSubForm):

    prefix='polldraft'

    @property
    def fields(self):
        if self.isAvailable():
            return Fields(IPollDraft)
        else:
            return Fields()

    def getContent(self):
        return self.parentForm.wizard.draft

    def isAvailable(self):
        return IPollDraft.providedBy(self.getContent())
