from Acquisition import aq_inner

from Products.Five import BrowserView

from zope.component import getMultiAdapter

class NewTagResponse(BrowserView):
    """ Required browser view for XML response
    """

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        
    def __call__(self, id):
        manage = getMultiAdapter((self.context, self.request), name="imagetags-manage")
        tag = manage.get_tag(id, create_on_fail=False)
        self.tag_id = id
        self.tag_box = '<![CDATA[%s]]>' % (manage.helper.tag_box(id=id, data=tag))
        self.tag_title = '<![CDATA[%s]]>' % (manage.helper.tag_title(id=id, data=tag))
        return self.index()
