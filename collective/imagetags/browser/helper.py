from zope.interface import implements
from Acquisition import aq_inner
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.Five import BrowserView

from plone.memoize import view

from collective.imagetags.browser.interfaces import IImageTagsHelper


class ImageTagsHelper(BrowserView):
    """
    imagetags-helper browser view with helper methods for manage and image browser views
    """
    implements(IImageTagsHelper)

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request

 
    def image_fields(self):
        """
        All the image fields available in current object
        """
        image_fields = getUtility(IVocabularyFactory, name='collective.imagetags.imagefields')(self.context)
        if image_fields is None:
            return []
        else:
            return [field.value for field in image_fields]

    @view.memoize
    def image(self):
        """
        The image field to use with tags (the first in self.image_fields() for the time being)
        TODO: Don't suppose there's a 'large' scale 
        """
        if self.has_image_field():
            field_name = self.image_fields()[0]
            return field_name
        else:
            return None

    def has_image_field(self):
        """
        Has this content type an image field with a stored image?
        """
        context = self.context
        image_fields = self.image_fields()
        if len(image_fields)>0:
            for field_name in image_fields:
                field = context.getField(field_name)
                if field.get_size(context)>0:
                    return True
                    
        return False
        
    @view.memoize
    def plone_version(self):
        """
        Returns major version number of Products.CMFPlone
        """
        try:
            from plone.app.upgrade import v40
            return 4
        except ImportError:
            return 3
        else:
            return 0
