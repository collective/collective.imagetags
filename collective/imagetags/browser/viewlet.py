from Acquisition import aq_inner
from plone.app.layout.viewlets import common
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from collective.imagetags.interfaces import IImageTagsSettings

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ImageTagsJSViewlet(common.ViewletBase):
    """ Viewlet to include a new <script /> tag in every page
    """
    
    def update(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IImageTagsSettings)
        enabled = settings.js_enabled
        selectors = []
        if enabled:
            rules = settings.rules
            rule = self.replace(rules)
            if rule!='':
                selectors.append(rule)

        inline_images = settings.inline_images
        if inline_images:
            selectors.append('#portal-columns img.imagetags-show')
        
        self.code = self.script(selectors)
        

    def replace(self, rules):
        context = aq_inner(self.context)
        ptype = context.Type()
        if not ptype:
            return False
            
        rule = self._get_rule(ptype, rules)
        if not rule:
            return False
        else:
            return rule

    def _get_rule(self, key, rules):
        if not rules:
            return None
        rule = [x.split('|')[1] for x in rules if x.split('|')[0]==key]
        if len(rule)>0:
            return rule[0]
        else:
            return None
            
    def script(self, selectors):
        if not selectors:
            return ''

        script = """jQuery(document).ready(function() {
            %s
        });""" % ('\n'.join(["ImageTags.replaceImageWithTags('%s');" % sel for sel in selectors]))
        return script
                
    index = ViewPageTemplateFile('templates/viewlet.pt')
