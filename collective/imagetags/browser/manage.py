from datetime import datetime
from Acquisition import aq_inner

from Products.Five import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements, alsoProvides, noLongerProvides
from zope.component import getMultiAdapter
from persistent.dict import PersistentDict
from Products.statusmessages.interfaces import IStatusMessage

from collective.imagetags.browser.interfaces import IManageTags
from collective.imagetags.interfaces import IImageWithTags

from collective.imagetags import imagetagsMessageFactory as _

ANNOTATIONS_KEY = u'ImageTags'

class ManageTags(BrowserView):
    """ Tag management browser view
    """
    
    implements(IManageTags)

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        self.helper = getMultiAdapter((self.context, self.request), name="imagetags-helper")
        self.default_image = self.helper.image()
        
    def __call__(self):
        """ This browser view can be called in a get/post request to remove 
            existing tags.
        """
        context = self.context
        request = self.request
        if 'form.widgets.remove' in request.form:
            ids = request.form['form.widgets.remove'];
            removed = self._remove_tags(ids=ids)
            
            if 'ajax' in request.form:
                array_id = [("'%s'" % id.encode('utf-8')) for id in ids]
                result = '{removed: [%s]}' % ', '.join(array_id)
                self.request.response.setHeader('content-type', 'text/javascript; charset=utf-8')
                self.request.response.write(result)
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

    
    def _mark_interface(self, action='add'):
        """ (un)Mark the object with a IImageWithTags marker interface 
        """
        context = self.context
        reindex = False
        if action=='add':
            if not IImageWithTags.providedBy(context):
                alsoProvides(context, IImageWithTags)
                reindex = True
        else:
            if IImageWithTags.providedBy(context):
                noLongerProvides(context, IImageWithTags)
                reindex = True
                
        if reindex:
            context.reindexObject()
        
    def _get_tags(self):
        """ Get the dictionary of tags for this object
        """
        context = self.context
        annotations = IAnnotations(context)
        tags = annotations.setdefault(ANNOTATIONS_KEY, PersistentDict())
        return tags

              
    def _remove_tags(self, ids=[]):
        """ Remove tags from the current object based on 'ids' parameter
        """
        tags = self.get_tags()
        removed = []
        for id in ids:
            if id in tags:
                removed.append(tags[id]['title'])
                del tags[id]
        if len(tags)==0:
            self._mark_interface(action='remove')
        return removed
                         
    def get_tag(self, id, create_on_fail=True):
        """ Get a given tag based on id.
            If create_on_fail = True, it will create a new placeholder (dictionary) if the tag is not found.
        """
        tags = self._get_tags()
        if not id in tags:
            if create_on_fail:
                tags[id] = PersistentDict()
            else:
                tags[id] = None
        return tags[id]

    def get_tags(self):
        """ Get all tags
        """
        return self._get_tags()
               
    def save_tag(self, data):
        """ Save a tag and create it (assigning an automatic id) if it's a new one
        """
        new_tag = False
        if not 'id' in data or data['id'] is None:
            id = datetime.utcnow().strftime('%Y%m%d.%H%M%S%f')
            data['id'] = id
            new_tag = True
        id = data['id']
        tag = self.get_tag(id)
        for x in data:
            if x != 'id' and x != 'ajax':
                if not x in tag or tag[x] != data[x]:
                    tag[x] = data[x]
                    
        self._mark_interface(action='add')
        if new_tag:
            message = _(u'Tag "${title}" added.', mapping={u'title': data['title']})
        else:
            message = _(u'Tag "${title}" updated.', mapping={u'title': data['title']})

        if not 'ajax' in data:
            IStatusMessage(self.request).addStatusMessage(message, type='info')

        return (id, tag, )
        
    def url(self):
        """ This browser view url
        """
        return '%s/@@%s' % (self.context.absolute_url(), self.__name__)
