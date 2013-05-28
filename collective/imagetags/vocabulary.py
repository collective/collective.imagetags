from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from Products.Archetypes.interfaces import IBaseObject

def ImageFieldsVocabularyFactory(context):
    """
    Returns a list of all the image fields available in current object
    """
    items = []
    if not IBaseObject.providedBy(context):
        return None

    image_fields = []
    schemata = context.Schemata()
    fieldsets = schemata.keys()
    for fieldset in fieldsets:
        for field in schemata[fieldset].fields():
            if field.getType() in ('plone.app.blob.subtypes.image.ExtensionBlobField', 'Products.Archetypes.Field.ImageField', ):
                image_fields.append(field)
                
    for field in image_fields:
        items.append(field.getName())
    
    return SimpleVocabulary.fromValues(items)

directlyProvides(ImageFieldsVocabularyFactory, IVocabularyFactory)


def ImprovedTemplatesVocabularyFactory(context):
    """Vocabulary factory with the three available default-Plone improved templates
       skin directories that are provided by this package.
    """
    items = (('News Item (newsitem_view)', 'imagetags_newsitem'),
             ('Image (image_view)', 'imagetags_image'),
             ('Fullscreen image (image_view_fullscreen)', 'imagetags_fullscreen'),
            )
    return SimpleVocabulary.fromItems(items)

directlyProvides(ImprovedTemplatesVocabularyFactory, IVocabularyFactory)
