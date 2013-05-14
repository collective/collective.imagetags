from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
import transaction

def updateKupu(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.imagetags_kupu.txt') is None:
        return

    # Add additional setup code here
    out = StringIO()
    portal = getSite()

    # Get kupu tool and update its paragraph_styles property
    kt = getToolByName(portal, 'kupu_library_tool', None)
    if kt:
        new_style = 'Show tags|img|imagetags-show'
        styles = kt.getParagraphStyles()
        if not new_style in styles:
            styles.append(new_style)
            kt.configure_kupu(parastyles=styles)
            transaction.savepoint()
            print >> out, "Updated paragraph_styles in kupu: %s" % new_style
        else:
            print >> out, "kupu already has %s in paragraph_styles" % new_style

    context.getLogger("collective.imagetags").info(out.getvalue())
    
    return out.getvalue()

