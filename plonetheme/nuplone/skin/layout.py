from zope.interface import Interface
from five import grok
from plonetheme.nuplone.skin.interfaces import NuPloneSkin

grok.templatedir("templates")

class Layout(grok.View):
    grok.context(Interface)
    grok.name("layout")
    grok.layer(NuPloneSkin)
    grok.template("layout")


