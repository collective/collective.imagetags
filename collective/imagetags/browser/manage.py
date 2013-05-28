from Acquisition import aq_inner

try:
    import json
except ImportError:
    import simplejson as json

from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.statusmessages.interfaces import IStatusMessage

from collective.imagetags.browser.interfaces import IManageTags
from collective.imagetags.adapters.interfaces import IImageTagsManager

from collective.imagetags import imagetagsMessageFactory as _


class ManageTags(BrowserView):
    """ Tag management browser view
    """
    
    implements(IManageTags)

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        self.helper = getMultiAdapter((self.context, self.request), name="imagetags-helper")
        self.default_image = self.helper.image()
        self.manager = IImageTagsManager(self.context)
        
    def __call__(self):
        """ This browser view can be called in a get/post request to remove 
            existing tags.
        """
        request = self.request
        if 'form.widgets.remove' in request.form:
            ids = request.form['form.widgets.remove']
            removed = self.manager.remove_tags(ids=ids)
            
            if 'ajax' in request.form:
                request.response.setHeader('content-type', 'application/json; charset=utf-8')
                response_body = {'removed': [id.encode('utf-8') for id in ids]}
                response_http = json.dumps(response_body)
                request.response.setHeader('content-length', len(response_http))
                return response_http
            else:
                count_removed = len(removed)
                if count_removed==1:
                    message = _(u'${count} tag removed.', mapping={u'count': count_removed})
                elif count_removed>1:
                    message = _(u'${count} tags removed.', mapping={u'count': count_removed})
                if count_removed>0:
                    IStatusMessage(self.request).addStatusMessage(message, type='info')
   
                return self.index()
                
        else:
            return self.index()

    def url(self):
        """ This browser view url
        """
        return '%s/@@%s' % (self.context.absolute_url(), self.__name__)
         
            
    # The following methods are now provided by IImageTagsManager adapter
    def get_tag(self, id, create_on_fail=False):
        """ Get a given tag based on id.
            If create_on_fail = True, it will create a new placeholder (dictionary) if the tag is not found.
        """
        return self.manager.get_tag(id, create_on_fail)

    def get_tags(self):
        """ Get all tags
        """
        return self.manager.get_tags()
        
    def get_sorted_tags(self):
        """ Sorted list of tags
        """
        return self.manager.get_sorted_tags()
               
    def save_tag(self, data):
        """ Save a tag and create it (assigning an automatic id) if it's a new one
        """
        return self.manager.save_tag(data)
        
