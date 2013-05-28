from Acquisition import aq_inner
from Products.Five import BrowserView
from zope.component import queryUtility, getMultiAdapter
from collective.imagetags import imagetagsMessageFactory as _
from zope.i18n.interfaces import ITranslationDomain


class JSLabels(BrowserView):
    """ Labels used in JavaScript (manage-tags.js)
    """

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        
    def __call__(self, *args, **kw):
        # Change content-type header for JavaScript
        response = self.request.response
        response.setHeader('Content-Type', 'application/x-javascript')

        # Create handy translate function
        td = queryUtility(ITranslationDomain, name='collective.imagetags')
        if td:
            tx = td.translate
        else:
            # Workaround for non-registered translation domain to prevent breaking
            tx = lambda(x): x

        # Get locales for decimalSeparator
        portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        locale = portal_state.locale()
        
        # Return JSON object as JavaScript source
        return """
/* Internationalized labels used for imagetags JavaScript interactions */

ImageTagsLabels = {
    tagFormTitle: '%s',
    removeLinkText: '%s',
    removeConfirmText: '%s',
    editLinkText: '%s',
    yesButtonText: '%s',
    noButtonText: '%s',
    saveButtonText: '%s',
    hyphenLabel: '%s',
    decimalSeparator: '%s'
};
        """ % (tx(_(u"Tag details")), 
               tx(_(u"Remove")),
               tx(_(u"Are you sure you want to remove this tag?")),
               tx(_(u"Edit")), tx(_(u"Yes")), tx(_(u"No")), tx(_(u'Save')),
               tx(_(u"imagetags.hyphen", default=u"-")),
               locale.numbers.symbols['decimal'],)
