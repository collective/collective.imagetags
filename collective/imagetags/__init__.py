  # -*- extra stuff goes here -*- 
from zope.i18nmessageid import MessageFactory

imagetagsMessageFactory = MessageFactory('collective.imagetags')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
