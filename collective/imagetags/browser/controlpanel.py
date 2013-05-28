from plone.app.registry.browser import controlpanel
from z3c.form import button
from plone.z3cform import layout
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from z3c.form.browser.checkbox import SingleCheckBoxFieldWidget, CheckBoxFieldWidget

from Products.statusmessages.interfaces import IStatusMessage
from collective.imagetags.interfaces import IImageTagsSettings
from collective.imagetags import imagetagsMessageFactory as _

class AdminRulesForm(controlpanel.RegistryEditForm):
    """ A configlet form for IImageSettings
        based on plone.app.registry.controlpanel
    """
    schema = IImageTagsSettings
    label = _(u"Image tags settings")

    # Copy and adaptation of controlpanel.RegistryEditForm
    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)

        # Special skin management for improved_templates field
        templates = data['improved_templates']
        if isinstance(templates, basestring):
            templates = [templates]

        available_templates = getUtility(IVocabularyFactory, name='collective.imagetags.templates')(self.context)
        skins = getToolByName(self.context, 'portal_skins')
        skinpaths = skins.getSkinSelections()
        for skin in skinpaths:
            path = skins.getSkinPath(skin)
            paths = [i.strip() for i in  path.split(',')]
            # First I got the list of skin layers (paths) of this skin
            for template in available_templates.by_value:
                if template in templates:
                    # If template is well positioned, make sure to add it into paths before 'plone_content'
                    if template in paths:
                        if 'plone_content' in paths:
                            if paths.index(template)>paths.index('plone_content'):
                                paths.remove(template)
                                paths.insert(paths.index('plone_content'), template)
                    else:
                        # template not in paths, add it
                        if 'plone_content' in paths:
                            paths.insert(paths.index('plone_content'), template)
                else:
                    # Template isn't selected, make sure to remove it from paths
                    if template in paths:
                        paths.remove(template)
            path = ','.join(paths)
            skins.addSkinSelection(skin, path)


        # Notify the user
        if changes:
            IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"), "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), self.control_panel_view))

    # Copy of the original Cancel button
    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"), "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), self.control_panel_view))

    
    def updateFields(self):
        """ Changes in form widgets
        """
        super(AdminRulesForm, self).updateFields()
        self.fields['improved_templates'].widgetFactory = CheckBoxFieldWidget
        self.fields['iframe_enabled'].widgetFactory = SingleCheckBoxFieldWidget
        self.fields['js_enabled'].widgetFactory = SingleCheckBoxFieldWidget
        self.fields['inline_images'].widgetFactory = SingleCheckBoxFieldWidget
        
    def updateWidgets(self):
        """ Set value for improved_templates field according to actual skin layers configuration
        """
        super(AdminRulesForm, self).updateWidgets()
        available_templates = getUtility(IVocabularyFactory, name='collective.imagetags.templates')(self.context)
        skins = getToolByName(self.context, 'portal_skins')
        path = skins.getSkinPath(skins.getDefaultSkin())
        paths = [i.strip() for i in  path.split(',')]
        include = False
        improved_templates = []
        for template in available_templates.by_value:
            # If template directory is available and (is before 'plone_content' or 'plone_content' isn't available)...
            include = (template in paths and 'plone_content' in paths and paths.index(template)<paths.index('plone_content')) or \
                      (template in paths and not 'plone_conent' in paths)
            
            # ... then check it
            if include:
                term = available_templates.getTerm(template)
                improved_templates.append(term.token)

        for template in self.widgets['improved_templates'].items:
            template['checked'] = template['value'] in improved_templates

    
class AdminRulesFormWrapper(layout.FormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
    panel layout.
    """
    form = AdminRulesForm
    index = ViewPageTemplateFile('templates/controlpanel_layout.pt')
