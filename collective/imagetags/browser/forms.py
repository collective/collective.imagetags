from zope.component import getMultiAdapter

from z3c.form import form, field, button
from z3c.form.interfaces import HIDDEN_MODE
from plone.app.z3cform.layout import wrap_form, FormWrapper

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from collective.imagetags.adapters.interfaces import IAddTag, \
    IImageTagsManager
from collective.imagetags import imagetagsMessageFactory as _

    
class AddTagForm(form.EditForm):
    """ Add / Update tag form
    """
    fields = field.Fields(IAddTag)
    label = _(u"Tag details")
    ignoreContext = True
    ignoreRequest = False
    
    def __init__(self, context, request):
        super(form.EditForm, self).__init__(context, request)
        self.helper = getMultiAdapter((self.context, request), name="imagetags-helper")
        
    def _updateWidgets(self):
        """ Hide some widgets and set value for 'field' widget
        """
        self.widgets['id'].mode = HIDDEN_MODE
        fields = self.widgets['field'].terms.terms._terms
        if len(fields)==1:
            self.widgets['field'].value = fields[0].value
            self.widgets['field'].mode = HIDDEN_MODE
        elif len(fields)==0:
            self.widgets['field'].mode = HIDDEN_MODE
        

    def updateWidgets(self):
        """ If 'id' parameter is in the request set values for widgets based
            on the chosen tag. 
        """
        super(form.EditForm, self).updateWidgets()
        self._updateWidgets()
        request = self.request
        id_field = 'id'
        if id_field in request.form:
            id = request.form[id_field]
            manager = IImageTagsManager(self.context)
            tag = manager.get_tag(id)
            if not tag is None:
                for x in tag:
                    self.widgets[x].value = tag[x]
                self.widgets['id'].value = id

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        """ Save (create or update) a tag
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        ajax = 'ajax' in self.request.form
            
        manager = IImageTagsManager(self.context)
        id, tag, new_tag = manager.save_tag(data)

        if not errors:
            #  Special treatment for ajax/non-ajax save
            if not ajax:
                if new_tag:
                    message = _(u"Tag '${title}' added.", mapping={u'title': tag['title']})
                else:
                    message = _(u"Tag '${title}' updated.", mapping={u'title': tag['title']})
                self.request.response.redirect('%s/@@imagetags-manage' % self.context.absolute_url())
                IStatusMessage(self.request).addStatusMessage(message, type='info')
            else:
                # Return XML response
                self.request.response.redirect('%s/@@imagetags-newtag?id=%s' % (self.context.absolute_url(), id))
               

class AddTagFormWrapper(FormWrapper):
    index = ViewPageTemplateFile('templates/form.pt')
    ajax = False
   
    def getId(self):
        return self.__name__.replace('.', '-')

        
AddTag = wrap_form(AddTagForm, __wrapper_class=AddTagFormWrapper)

