from Acquisition import aq_inner

from Products.Five import BrowserView
from zope.component import getMultiAdapter

from collective.imagetags.adapters.interfaces import IImageTagsManager

class NewTagResponse(BrowserView):
    """ Required browser view for XML response
    """

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        
    def __call__(self, id):
        manager = IImageTagsManager(self.context)
        tag = manager.get_tag(id)
        image = getMultiAdapter((self.context, self.request), name="imagetags-img")
        self.tag_id = id
        self.tag_box = '<![CDATA[%s]]>' % (image.tag_box(id=id, data=tag))
        self.tag_title = '<![CDATA[%s]]>' % (image.tag_title(id=id, data=tag))
        return self.index()
