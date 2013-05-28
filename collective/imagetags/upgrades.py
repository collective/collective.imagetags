from Products.CMFCore.utils import getToolByName
from collective.imagetags.interfaces import IImageWithTags
from collective.imagetags.adapters.interfaces import IImageTagsManager

import logging

def migrate_1001_1010(context, logger=None):
    """ Replace all dots in tag ids with hyphens.
        This slightly enhances performance especially in JavaScript
        and also simplifies code
    """
    if logger is None:
        logger = logging.getLogger('collective.imagetags')
        
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog(object_provides=IImageWithTags.__identifier__)
    for brain in brains:
        object = brain.getObject()
        manager = IImageTagsManager(object)
        tags = manager.get_tags()
        for tag_id in tags:
            if '.' in tag_id:
                tag_data = tags[tag_id]
                tag_data['id'] = tag_id.replace('.', '-')
                manager.remove_tags(ids=[tag_id,])
                manager.save_tag(tag_data)
                
    logger.info('%s objects migrated with new tag ids' % len(brains))


