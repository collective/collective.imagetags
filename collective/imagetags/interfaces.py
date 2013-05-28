from zope.interface import Interface
from zope import schema
from collective.imagetags import imagetagsMessageFactory as _


class IImageWithTags(Interface):
    """
    Marker interface for objects with tagged images
    """

class IImageTagsLayer(Interface):
    """
    A layer specific to this product. It is registered using browserlayer.xml
    """
    
class IImageTagsSettings(Interface):
    """ ImageTags admin schema for control panel settings
    """
    improved_templates = schema.List(
                                title=_(u"Improved templates"),
                                description=_(u"Default Plone templates to be overriden with tagged-images."),
                                required=False,
                                value_type=schema.Choice(title=_(u"Template"), vocabulary='collective.imagetags.templates'))

    iframe_enabled = schema.Bool(
                            title=_(u"Use <iframe />"),
                            description=_(u"Show 'Embed code (HTML)' code snippets in 'Tags' tab. Don't forget to add 'iframe' "
                                            "as a valid tag in safe_html  of portal_transforms. "
                                            "Notice that this setting won't prevent displaying iframes in documents."),
                            required=False,
                            default=True)

    iframe_taglist_height = schema.Int(
                                   title=_(u"Tag list height"),
                                   description=_(u"Number of pixels assigned to the 'Tagged' box when calculating iframe height."),
                                   required=True,
                                   default=20)

    inline_images = schema.Bool(
                           title=_(u"Replace inline images"),
                           description=_(u"Replace all inline images (inside text content or portlets) styled with 'imagetags-show' class attribute."),
                           required=False,
                           default=False)
                           

    js_enabled = schema.Bool(
                        title=_(u"Enable JavaScript replacement rules"),
                        description = _(u"help_imagetags_settings_editform",
                                        default=u"Use these CSS rules below to replace standard images -in content types- with tagged images.\n"
                                                 "These replacement will be made via JavaScript. Providing a non-JavaScript option is better.\n"
                                                 "If you prefer to us a non-JavaScript option you will have to modify the view templates of the target "
                                                 "content types by changing context.tag() call for context.@@imagetags-img(name='image_mini')."
                                                 "You can use any available scale in image or the full image itself. "
                                                 "Alternatively you can enable any of the default Plone 'Improved templates' above."),
                        required=False,
                        default=False)
                        
    rules = schema.List(
            title=_(u"JavaScript replacement rules"),
            description=_(u"Add a replacement rule in each line with this format: 'Portal type|CSS img selector'."),
            required=False,
            default=[u'News Item|.newsImageContainer>a>img', u'Image|#content-core>a>img',],
            value_type=schema.TextLine(title=_(u"Rule")))

