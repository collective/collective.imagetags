from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getMultiAdapter
from zope.interface import implements

from collective.imagetags.browser.interfaces import IImageTagsImage

class ImageTagsImage(BrowserView):
    """ Used to display the tagged image (i.e., the image with all its tags)
    """

    implements(IImageTagsImage)

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        self.embedded = True
        manage = getMultiAdapter((context, request), name="imagetags-manage")
        self.get_tags = manage.get_tags
        self.helper = manage.helper
        self.default_image = manage.default_image
        self.iframe_enabled = self.helper.settings.iframe_enabled
        
        
    def __call__(self, name=None, embedded=True, iframe=False, full_screen=True):
        """ When called, set self.image according to "name" parameter
        """
        self.iframe = iframe
        self.embedded = embedded or iframe
        self.full_screen = full_screen
        if not name is None:
            parts = name.split('_')
            field_name = parts[0]
            scale_name = ''
            if len(parts)>1:
               scale_name= parts[1]
            field = self.context.getField(field_name)
            if field:
                if scale_name != '' and scale_name in field.getAvailableSizes(self.context):
                    self.image = field.getScale(self.context, scale=scale_name)
                else:
                    self.image = field.get(self.context)
                    
                self.full_image = field_name
                
        else:
            self.image = self.default_image


        return self.index()
        
