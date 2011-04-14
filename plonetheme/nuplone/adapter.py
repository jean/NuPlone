from zope.annotation.interfaces import IAnnotations
from zope.i18n import translate
from webhelpers.html.builder import literal
from Products.statusmessages import adapter
from Products.statusmessages import STATUSMESSAGEKEY
HTMLMESSAGEKEY = 'literal-messages'

import logging
logger = logging.getLogger('plonetheme/nuplone/adapter.py')

class StatusMessage(adapter.StatusMessage):
    """ Overrides the standard IStatusMessage adapter to provide literal string
        support (i.e strings with the '__html__' class).

        This allows us to send html as statusmessages, without it being escaped
        by Chameleon.
    """ 
    def addHTML(self, text, type=u'info'):
        """ Add a HTML status message.
        """
        context = self.context
        annotations = IAnnotations(context)
        text = translate(text, context=context)
        old = annotations.get(
                        HTMLMESSAGEKEY,
                        context.cookies.get(HTMLMESSAGEKEY)
                        )
        value = adapter._encodeCookieValue(text, type, old=old)
        context.response.setCookie(HTMLMESSAGEKEY, value, path='/')
        annotations[HTMLMESSAGEKEY] = value

    def show(self):
        """ Removes all status messages (including HTML) and returns them 
            for display.
        """
        context = self.context
        annotations = IAnnotations(context)
        msgs = annotations.get(STATUSMESSAGEKEY,
                                context.cookies.get(STATUSMESSAGEKEY))
        msgs = msgs and adapter._decodeCookieValue(msgs) or []

        html_msgs = annotations.get(HTMLMESSAGEKEY,
                                context.cookies.get(HTMLMESSAGEKEY))
        html_msgs = html_msgs and adapter._decodeCookieValue(html_msgs) or []
        for msg in html_msgs:
            msg.message = literal(msg.message)

        value = msgs + html_msgs
        
        # clear the existing cookie entries, except on responses that don't
        # actually render in the browser (really, these shouldn't render
        # anything so we shouldn't get to this message, but some templates
        # are sloppy).
        if self.context.response.getStatus() not in (301, 302, 304):
            context.cookies[STATUSMESSAGEKEY] = None
            context.response.expireCookie(STATUSMESSAGEKEY, path='/')
            annotations[STATUSMESSAGEKEY] = None

            context.cookies[HTMLMESSAGEKEY] = None
            context.response.expireCookie(HTMLMESSAGEKEY, path='/')
            annotations[HTMLMESSAGEKEY] = None
        
        return value
    
    addHTMLStatusMessage = addHTML
    showStatusMessages = show
