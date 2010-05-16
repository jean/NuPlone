from Acquisition import aq_inner
from zope.interface import Interface
from five import grok
from plonetheme.nuplone import MessageFactory as _
from plonetheme.nuplone.utils import setLanguage
from Products.statusmessages.interfaces import IStatusMessage


class SwitchLanguage(grok.View):
    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("switch-language")

    def render(self):
        flash=IStatusMessage(self.request).addStatusMessage
        if setLanguage(self.request, self.context):
            flash(_("message_switch_language", default=u"Language updated"), "success")
        else:
            flash(_("message_switch_language_error", default=u"Failed to switch language"), "error")

        self.request.response.redirect(aq_inner(self.context).absolute_url())
