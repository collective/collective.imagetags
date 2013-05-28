from datetime import datetime
from Acquisition import aq_inner

from zope.annotation.interfaces import IAnnotations
from zope.interface import implements, alsoProvides, noLongerProvides
from persistent.dict import PersistentDict

from collective.imagetags.interfaces import IImageWithTags
from collective.imagetags.adapters.interfaces import IImageTagsManager

ANNOTATIONS_KEY = u'ImageTags'

class ImageTagsManager(object):
    """ Tag management adapter
    """
    
    implements(IImageTagsManager)
    
    def __init__(self, context):
        """Constructor"""
        self.context = aq_inner(context)

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
        
    def _storage(self):
        """ Get the dictionary of tags for this object
        """
        context = self.context
        annotations = IAnnotations(context)
        tags = annotations.setdefault(ANNOTATIONS_KEY, PersistentDict())
        return tags

              
    def remove_tags(self, ids=[]):
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
                         
    def get_tag(self, id, create_on_fail=False):
        """ Get a given tag based on id.
            If create_on_fail = True, it will create a new placeholder (dictionary) if the tag is not found.
        """
        tags = self._storage()
        if not id in tags:
            if create_on_fail:
                tags[id] = PersistentDict()
            else:
                tags[id] = None
        return tags[id]

    def get_tags(self):
        """ Get all tags
        """
        return self._storage()
        
    def get_sorted_tags(self):
        """ Sorted list of tags
        """
        tags = self._storage()
        return sorted(tags.items(), key=lambda x: x[1]['title'])
               
    def save_tag(self, data):
        """ Save a tag and create it (assigning an automatic id) if it's a new one
        """
        new_tag = False
        if not 'id' in data or data['id'] is None:
            now = datetime.utcnow()
            id = '%s%s' % (now.strftime('%Y%m%d-%H%M%S'), now.microsecond)
            data['id'] = id
            new_tag = True
        id = data['id']
        tag = self.get_tag(id, create_on_fail=True)
        for x in data:
            if x != 'id' and x != 'ajax':
                if not x in tag or tag[x] != data[x]:
                    tag[x] = data[x]
                    
        self._mark_interface(action='add')
        return (id, tag, new_tag, )
