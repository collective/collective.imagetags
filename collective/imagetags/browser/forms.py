from zope.interface import implements
from zope.component import getMultiAdapter

from z3c.form import form, field, button
from z3c.form.browser.text import TextFieldWidget
from z3c.form.interfaces import HIDDEN_MODE
from plone.app.z3cform.layout import wrap_form, FormWrapper

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.imagetags.browser.interfaces import IAddTag, IAddAjaxTag
from collective.imagetags import imagetagsMessageFactory as _


class AddTagAdapter(object):
    """ Dummy adapter required by z3c.form but isn't really used to persist data.
        Data is persisted in special annotation in the object.
    """
        
    implements(IAddTag)

    id = ''
    title = ''
    url = ''
    x = 0
    y = 0
    ajax = 0

    def __init__(self, context):
        self.context = context
    
class AddTagForm(form.EditForm):
    """ Add / Update tag form
    """
    fields = field.Fields(IAddTag)
    label = _(u"Tag details")
    ignoreContext = True
    ignoreRequest = False
    prefix = 'regform.'
    
    def __init__(self, context, request):
        super(form.EditForm, self).__init__(context, request)
        self.manager = getMultiAdapter((self.context, request), name="imagetags-manage")
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
            tag = self.manager.get_tag(id, False)
            if not tag is None:
                prefix = '%swidgets' % (self.prefix)
                for x in tag:
                    self.widgets[x].value = tag[x]
                self.widgets['id'].value = id

    @button.buttonAndHandler(_('Save'), name='save')
    def handleApply(self, action):
        """ Save (create or update) a tag
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        ajax = 'ajax' in data
            
        id, tag = self.manager.save_tag(data)
           
        #  Special treatment for ajax/non-ajax save
        if not errors:
            if not ajax:
                self.request.response.redirect('%s/@@%s' % (self.context.absolute_url(), self.manager.__name__))
            else:
                self.request.response.redirect('%s/@@imagetags-newtag?id=%s' % (self.context.absolute_url(), id))
               

class AddTagFormWrapper(FormWrapper):
    index = ViewPageTemplateFile('templates/form.pt')
    ajax = False
   
    def getId(self):
        return self.__name__.replace('.', '-')
        
AddTag = wrap_form(AddTagForm, __wrapper_class=AddTagFormWrapper)

class AddTagAjaxForm(AddTagForm):
    """ Special Add / Update tag form for AJAX interaction
    """
    fields = field.Fields(IAddTag, IAddAjaxTag)
    label = _(u"Tag details")
    ignoreContext = True
    ignoreRequest = True
    prefix = 'form.'

    def updateWidgets(self):
        super(AddTagForm, self).updateWidgets()
        self._updateWidgets()
        # Hide x, y widgets (they are set via click event)
        self.widgets['x'].mode = HIDDEN_MODE
        self.widgets['y'].mode = HIDDEN_MODE
        # Hide ajax field (just a "marker" field)
        self.widgets['ajax'].mode = HIDDEN_MODE
        

class AddTagAjaxFormWrapper(AddTagFormWrapper):
    index = ViewPageTemplateFile('templates/form-ajax.pt')
    #ajax = True

AddTagAjax = wrap_form(AddTagAjaxForm, __wrapper_class=AddTagAjaxFormWrapper)
