from zope.interface import Interface
from zope import schema

from collective.imagetags import imagetagsMessageFactory as _

class IAddTag(Interface):
    """
    Form to add a new image tag
    """

    id = schema.TextLine(title=_(u"Id"),
                         required=False)
                         
    field = schema.Choice(title=_(u"Image field"),
                          description=_(u"Image field you want to add this tag"),
                          vocabulary='collective.imagetags.imagefields',
                          required=True)


    title = schema.TextLine(title=_(u"Title displayed in the tag"),
                            required=True)

    url = schema.URI(title=_(u"Link for the tag"),
                     required=False)

    x = schema.Float(title=_(u"X position"),
                     description=_(u"Position in the X axis of the center of the box (0-100%)"),
                     min=0.0,
                     max=100.0)

    y = schema.Float(title=_(u"Y position"),
                     description=_(u"Position in the Y axis of the center of the box (0-100%)"),
                     min=0.0,
                     max=100.0)
                     
class IAddAjaxTag(Interface):
    """
    Fields for ajax-submitted form
    """
    ajax = schema.Int(title=u"Ajax submitted",
                      default=1,
                      required=False)

class IImageTagsHelper(Interface):
    """
    imagetags-helper interface with helper methods for manage and image browser views
    """
    
    def portal_url():
        """ Returns portal_url """
        
    def image_fields():
        """ All the image fields available in current object """

    def image():
        """ The field to use with tags """
        
    def available_sizes(field_name):
        """ Available scale names for the given field in current object """

    def has_image_field():
        """ Has this content type an image field? """
        
    def tag_box(data):
        """ A call to a page template file """

    def tag_title(id, data):
        """
        A call to a pagetemplate file
        """

class IManageTags(Interface):
    """
    imagetags-manage view interface
    Tag management browser view
    """

    def get_tag(id, create_on_fail=True):
        """ Gets / creates a specific tag """

    def get_tags():
        """ Gets all the tags for the object """
        
    def save_tag(data):
        """ Saves a tag with the passed data """
        
    def url():
        """ URL of the current view """
        
class IImageTagsImage(Interface):
    """
    imagetags-image view interface
    Used to display the tagged image (i.e., the image with all its tags)
    """
