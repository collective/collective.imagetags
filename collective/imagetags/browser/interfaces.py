from zope.interface import Interface, Attribute

                     
class IImageTagsHelper(Interface):
    """
    imagetags-helper interface with helper methods for manage and image browser views
    """
    
    def image_fields():
        """ All the image fields available in current object """

    def image():
        """ The field to use with tags """
        
    def has_image_field():
        """ Has this content type an image field? """
        
    def plone_version():
        """ Returns major version number of Products.CMFPlone """
        

class IManageTags(Interface):
    """
    imagetags-manage view interface
    Tag management browser view
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
        
    def url():
        """ URL of the current view """


        
class IImageTagsImage(Interface):
    """
    imagetags-image view interface
    Used to display the tagged image (i.e., the image with all its tags)
    """
    
    embedded = Attribute("""The image is embedded inside another view or is this the manage view""")
    
    tags = Attribute("""A sorted list of tags""")
    
    default_image = Attribute("""Default image in case no specific image is defined""")
    
    iframes_enabled = Attribute("""iframes_enabled setting""")
    
    taglist_height = Attribute("""iframe_taglist_height setting""")
    
    def field_name(field_name):
        """ Real name of the field name, not a scale name
        """
    
    def available_sizes(field_name):
        """ Available scale names for the given field in current object """

    def tag_box(data):
        """ A call to a page template file """

    def tag_title(id, data):
        """
        A call to a pagetemplate file
        """

    def portal_url():
        """ Returns portal_url """
        

