from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getMultiAdapter, queryUtility
from zope.interface import implements

from plone.registry.interfaces import IRegistry

from collective.imagetags.browser.interfaces import IImageTagsImage
from collective.imagetags.interfaces import IImageTagsSettings
from collective.imagetags.adapters.interfaces import IImageTagsManager
    
from plone.memoize import view

class ImageTagsImage(BrowserView):
    """ Used to display the tagged image (i.e., the image with all its tags)
    """

    implements(IImageTagsImage)

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        self.embedded = True
        # Get tag manager to get sorted tags
        manager = IImageTagsManager(self.context)
        self.tags = manager.get_sorted_tags()
        # Get helper to get default image
        helper = getMultiAdapter((self.context, self.request), name="imagetags-helper")
        self.default_image = helper.image()
        # Get settings from portal_registry for ImageTags 
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IImageTagsSettings)
        self.iframe_enabled = settings.iframe_enabled
        self.taglist_height = settings.iframe_taglist_height
        
        
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
            if not field:
                # Workaround for old way of embedding iframes
                scale_name = field_name
                field_name = self.default_image
                field = self.context.getField(field_name)
            if field:
                if scale_name != '' and scale_name in field.getAvailableSizes(self.context):
                    self.image = '%s_%s' % (field_name, scale_name)
                else:
                    self.image = field_name
                    
                self.full_image = field_name
                
        else:
            pass

        return self.index()
        
    @view.memoize
    def field_name(self, field_name):
        """ Returns the real name of the field name, not a scale name
        """
        if '_' in field_name:
            field_name = field_name.split('_')[0]
        return field_name
        
    def available_sizes(self, field_name):
        """ List of (scale_name, (width, height)) for image field (denoted by field_name)
            in current object
        """
        field_name = self.field_name(field_name)
        field = self.context.getField(field_name)
        sizes = field.getAvailableSizes(self.context)

        # Sorting function
        def my_sort(x,y):
            return sizes[x][0]-sizes[y][0]

        keys = sizes.keys()
        keys.sort(my_sort)
        
        sorted_sizes = []
        # remove zero sizes
        for size in keys:
            if sizes[size][0] > 0:
               scale = field.getScale(self.context, scale=size)
               sorted_sizes.append((size, (scale.width, scale.height)))
         
        # TODO: We hide original for the time being because there's no
        # easy way to identify field_name / scale_name when embedding an iframe
        #image = field.get(self.context)
        #sorted_sizes.append(('original', (image.width, image.height)))
        return sorted_sizes

    
    def tag_box(self, id, data):
        """
        A call to a pagetemplate file
        """
        template = ViewPageTemplateFile('templates/tag_box.pt')
        return template(self, id=id, data=data)
        
    def tag_title(self, id, data):
        """
        A call to a pagetemplate file
        """
        template = ViewPageTemplateFile('templates/tag_title.pt')
        return template(self, id=id, data=data)

    @view.memoize
    def portal_url(self):
        """ Helper method required by tag_box
        """
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        return portal_state.portal_url()

