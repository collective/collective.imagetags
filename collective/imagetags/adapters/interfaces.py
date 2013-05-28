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

class IImageTagsManager(Interface):
    """
    imagetags-manage view interface
    Tag management browser view
    """

    def remove_tags(ids=[]):
        """ Remove tags based on 'ids' parameter
        """
        
    def get_tag(id, create_on_fail=False):
        """ Gets / creates a specific tag """

    def get_tags():
        """ Gets all the tags for the object """
        
    def get_sorted_tags():
        """ Sorted list of tags
        """

    def save_tag(data):
        """ Saves a tag with the passed data """
