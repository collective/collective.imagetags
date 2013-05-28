from zope.interface import implements
from collective.imagetags.adapters.interfaces import IAddTag

class AddTagAdapter(object):
    """ Dummy adapter required by z3c.form but isn't really used to persist data.
        Data is persisted in special annotation in the object.
    """
        
    implements(IAddTag)

    id = ''
    title = ''
    url = ''
    x = 0
    y = 0

    def __init__(self, context):
        self.context = context
    
