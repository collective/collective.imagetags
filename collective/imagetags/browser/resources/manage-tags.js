/* collective.imagetags JavaScript for managing tagged images */

jQuery(document).ready(function() {
    if(jQuery('.tag-image-wrapper').length) {
        jQuery('.tag-manage').removeClass('tag-manage').addClass('tag-manage-inline');
        jQuery('#imagetags-form, #imagetags-manage').hide();
        jQuery('#tag-start-tagging').show().click(ImageTags.startTagging);
        jQuery('#tag-stop-tagging').click(ImageTags.stopTagging);
        // auto-select input fields
        jQuery('.tag-embed-code input').focus(function(event) {event.target.select();});
        ImageTags.prepareEmbedOptions()
    }

});



/* ImageTags object with all required functions
 * 
 */

// Backup existing ImageTags to be used later (at the bottom).

ImageTags_bak = window['ImageTags'] || {};
ImageTags = {
    version: '1.0',
    title: 'ImageTags',
    description: 'Client side managing of image tags',
    hyphen: ' - ',
    draggableConfig: {revert: false, cancel: 'span.tag-link-title'},
    saveButton: 'Save',

    startTagging: function(event) {
        /* When "Start tagging" link is pressed, perform the following actions
         */
        if(event) {
            event.preventDefault();
            event.stopPropagation();
        }
        // Hide #tag-start link and show tag-stop link
        jQuery('#tag-start-tagging').hide();
        jQuery('#tag-stop-tagging').show();
        // Find the form and bind its "onsubmit" event
        var formContainer = jQuery('#ajax-form');
        var form = formContainer.find('form');
        form.submit(ImageTags.submitForm);
        // Add onblur event to required fields (span.required is sibling of div.widget with input children)
        form.find('.fieldRequired').next().find('input').keyup(ImageTags.checkRequired);
        // Add a special tag-tagging class and bind click event on the wrapper
        jQuery('.tag-image-wrapper').addClass('tag-tagging').click(ImageTags.onWrapperClick);
        // Turns boxes (a.tag-link) into draggable, bind the stop event and add a special class to them
        ImageTags.draggableConfig['stop'] = ImageTags.onBoxStopDragging;
        ImageTags.draggableConfig['start'] = ImageTags.onBoxStartDragging;
        ImageTags.turnDraggable(jQuery('.tag-image-wrapper a.tag-link'));
        // Add a special tag-tagging class to the a.tag-plain links
        jQuery('.tag-tag-list').addClass('tag-tagging');
        // Bind click event to a.tag-edit links
        ImageTags.turnEditable(jQuery('.tag-edit'));
        // Bind click event to a.tag-remove links
        ImageTags.turnRemovable(jQuery('.tag-remove'));
        // Re-set ImageTags.hyphen and ImageTags.saveButton values based on markup (it could change according to translations)
        ImageTags.hyphen = jQuery('#imagetags-hyphen').text();
        ImageTags.saveButton = form.find('input.submit-widget').hide().addClass('allowMultiSubmit').val()
        // Bind click event to a.tag-link-plain to disable real links
        ImageTags.preventRealLink(jQuery('.tag-link-plain'));
    },
    
    
    stopTagging: function(event) {
        /* When "Stop tagging" link is pressed, restore some events and elements to their originals
         */
        if(event) {
            event.preventDefault();
            event.stopPropagation();
        }
        // Show / Hide Start / Stop links
        jQuery('#tag-start-tagging').show();
        jQuery('#tag-stop-tagging').hide();
        // Remove class and click event handler
        jQuery('.tag-image-wrapper').removeClass('tag-tagging').unbind('click', ImageTags.onWrapperClick);
        // Destroy draggable objects
        jQuery('.tag-image-wrapper a.tag-link').draggable('destroy');
        // Remove class of tag list
        // Unbind click events of links
        jQuery('.tag-tag-list').removeClass('tag-tagging');
        jQuery('.tag-edit').unbind('click', ImageTags.onEditLinkClick);
        jQuery('.tag-remove').unbind('click', ImageTags.onRemoveLinkClick);
        jQuery('.tag-link-plain').unbind('click', ImageTags.onRealLinkClick);
        // Restore the original linksOverOut behavior to tag list (hover -> show box).
        ImageTags.linksOverOut();
    },
    
    turnDraggable: function(collection) {
        /* Turn collection into draggable according to ImageTags configuration
         */
        collection.draggable(ImageTags.draggableConfig);
    },
    
    turnEditable: function(collection) {
        /* Turn collection into editable (i.e. bind click event)
         */
        collection.click(ImageTags.onEditLinkClick);
    },
    
    turnRemovable: function(collection) {
        /* Turn collection into removable (i.e. bind click event)
         */
        collection.click(ImageTags.onRemoveLinkClick);
    },

    preventRealLink: function(collection){
        /* Prevent click event propagation an default to collection
         */
        collection.click(ImageTags.onRealLinkClick);
    },
  
    onBoxStopDragging: function(event, ui) {
        /* Called when a tag-link box is dropped  
         */ 
        // Get the wrapper and take its measures
        var wrapper = jQuery('.tag-image-wrapper');
        var wWidth = wrapper.width();
        var wHeight = wrapper.height();
        // Get the tag-link box and get its new position (X,Y center point)
        var box = ui.helper;
        box.removeClass('tag-link-active');
        var newX = ui.position.left + box.width()/2;
        var newY = ui.position.top + box.height()/2;
        // Calculate real final position (0%<=position<=100%)
        var finalPosition = {}
        if(newX<0) {
            newX = 0;
            finalPosition['left'] = (newX - box.width()/2) + 'px';
        }
        if(newX>wWidth) {
            newX = wWidth;
            finalPosition['left'] = (newX - box.width()/2) + 'px';
        }
        if(newY>wHeight) {
            newY = wHeight;
            finalPosition['top'] = (newY - box.height()/2) + 'px';
        }
        if(newY<0) {
            newY = 0;
            finalPosition['top'] = (newY - box.height()/2)+ 'px';
        }
        // If "desired" position is out of limits, re-place the box
        if(finalPosition['top'] !== undefined || finalPosition['left'] !== undefined) {
            box.animate(finalPosition, 'fast');
        }
        // Translate X,Y into percentages
        var perX = Math.min(100, Math.max(0, (newX/wWidth*100).toFixed(1)));
        var perY = Math.min(100, Math.max(0, (newY/wHeight*100).toFixed(1)));
        // Prepare data to be sent to server
        var id = box.attr('id').replace('image-tag-', '').replace('-', '.');
        var title = box.find('.tag-link-title').text();
        var url = box.attr('href') || '';
        var form = jQuery('#ajax-form form');
        var data = {'x': perX, 'y': perY, 'id': id, 'title': title, 'url': url, 'ajax': 1};
        // Pre-load form (invisibly) to be submitted.
        ImageTags.loadForm(data);
        // Post the data to the server.
        ImageTags.submitForm();
    },
    
    onBoxStartDragging: function(event, ui) {
        /* Called when dragging starts. Used to change class of object being dragged 
         */
        ui.helper.addClass('tag-link-active');
    },
    
    onWrapperClick: function(event) {
        /* Click event handler for .tag-image-wrapper to create / update tag.
         */
        event.preventDefault();
        event.stopPropagation();
        var target = jQuery(event.target);
        var box = target.closest('a.tag-link');
        var isBox = box.length > 0;
        if(isBox) {
            // If click was made on a box, edit it
            ImageTags.editExistingTagBox(box);
        } else {
            // If click was made on a free area of the wrapper, create a new tag
            ImageTags.newTagBox(event);
        }
    },

    editExistingTagBox: function(box) {
        /* Edit a tag-link box 
         */
        // Get wrapper and offset to take box x,y position
        var wrapper = box.closest('.tag-image-wrapper');
        var wWidth = wrapper.width();
        var wHeight = wrapper.height();
        var position = box.position()
        var newX = position.left /*- offsetW.left*/ + box.width()/2;
        var newY = position.top /*- offsetW.top*/ + box.height()/2;
        // Translate X,Y into percentages
        var perX = Math.min(100, Math.max(0, (newX/wWidth*100).toFixed(1)));
        var perY = Math.min(100, Math.max(0, (newY/wHeight*100).toFixed(1)));
        // Pre-load data on the form
        var id = box.attr('id').replace('image-tag-', '').replace('-','.');
        var title = box.find('.tag-link-title').text();
        var url = box.attr('href');
        box.addClass('tag-link-active');
        // Display the edit tag details form
        ImageTags.loadForm({x: perX, y: perY, 'id': id, 'title': title, 'url': url});
        ImageTags.showForm(box);
    },

    onEditLinkClick: function(event) {
        /* If image-tag-edit links are used instead of boxes, 
         * edit the boxes anyway
         */
        event.preventDefault();
        event.stopPropagation();
        // Get the box and edit it
        var id = event.target.id.replace('image-tag-edit-', 'image-tag-');
        ImageTags.editExistingTagBox(jQuery('#' + id));
    },
    
    onRemoveLinkClick: function(event) {
        /* If image-tag-remove links are clicked
         * remove the link via AJAX
         */
        event.preventDefault();
        event.stopPropagation();
        // Call to confirm dialog
        var confirmDiv = jQuery('#imagetags-confirm-remove');
        var yes = confirmDiv.find('span').first().text();
        var no = confirmDiv.find('span').last().text()
        var buttons = {}
        buttons[no] = function() {
            jQuery(this).dialog('close');
        };
        buttons[yes] = function() {
            jQuery(this).dialog('close');
            jQuery.get(event.target.href + '&ajax:int=1', ImageTags.onRemoveSuccess);
        };
        confirmDiv.dialog({
            title: confirmDiv.find('em').text(), 
            resizable: false,
            buttons: buttons,
            modal: true
        })
    },

    onRealLinkClick: function(event) {
        /* When tagging, clicking on real links shouldn't behave as regular links
         */
        event.preventDefault();
        event.stopPropagation();
    },
    

    newTagBox: function(event) {
        /* When click on image-wrapper to create a new tag
         * get the x,y percentage of the click event 
         * and show the edit tag details form 
         */        
        var wrapper = jQuery(event.target);
        var offsetW = wrapper.offset();
        var wWidth = wrapper.width();
        var wHeight = wrapper.height();
        var newX = event.pageX - offsetW.left;
        var newY = event.pageY - offsetW.top;
        // Turn X,Y into percentages
        var perX = Math.min(100, Math.max(0, (newX/wWidth*100).toFixed(1)));
        var perY = Math.min(100, Math.max(0, (newY/wHeight*100).toFixed(1)));
        ImageTags.loadForm({x: perX, y: perY});
        ImageTags.showForm();
    },
    
     
    loadForm: function(config) {
        /* Load the edit tag details form with all the passed data
         */
        var form = jQuery('#ajax-form');
        var prefix = 'form.widgets.';
        // Set default values in the form
        jQuery.each(config, function(field, value) {
            form.find('input[name=' + prefix + field + ']').val(value);
        });
    },

    showForm: function(box) {
        /* Display the edit tag details form
         */
        var formContainer = jQuery('#ajax-form');
        // Get the title
        var title = formContainer.find('h2').hide().text();
        // onclose function
        var onclose = function(event, ui) {
            ImageTags.resetForm();
            if(box) {
                box.removeClass('tag-link-active');
            }
        };
        // Display the form dialog
        buttons = {};
        buttons[ImageTags.saveButton] = ImageTags.submitForm;
        formContainer.dialog({
            title: title, 
            resizable: false,
            close: onclose,
            open: function(event, ui) {
                jQuery(this).find('input[type!=hidden]').first().focus();
            },
            buttons: buttons
        });
    },
    
    submitForm: function(event) {
        /* Click event handler for the Save button in dialog or 
         * for the onsubmit event in form
         */
        var onPostSuccess;
        if(event) {
            event.preventDefault();
            event.stopPropagation();
            onPostSuccess = ImageTags.onPostSuccess;
        } else {
            onPostSuccess = ImageTags.resetForm;
        }
        var form = jQuery('#ajax-form form');
        // Check if there's any missing value field 
        var missing = form.find('.field-missing-value');
        if(missing.length > 0) {
            missing.focus();
            return;
        }
        var button = form.find('input[type=submit]')[0];
        
        // Post data to the server
        jQuery.post(form.attr('action'), form.serialize() + '&' + button.name + '=' + button.value, onPostSuccess);
    },
    
    resetForm: function() {
        /* Reset the form to empty values (except for the "field"-named field)
         */
        var container = jQuery('#ajax-form');
        container.find('input[type!=submit],select,textarea').not('input[name$=field:list],input[name$=ajax]').val('');
        container.find('.field-missing-value').removeClass('field-missing-value');
    },

    onPostSuccess: function(data, status, request) {
        /* Called after submission success
         */
        // Close (and reset) the form
        jQuery('#ajax-form').dialog('close');
        ImageTags.resetForm();
        // Take the response data and show/update boxes or tags
        var root = jQuery(request.responseXML.documentElement);
        var id = root.attr('id');
        var boxHTML = root.find('box');
        var titleHTML = root.find('title');
        var safeId = id.replace('.','-');
        var box = jQuery('#image-tag-' + safeId);
        var plainTags;
        if(box.length>0) {
            box.replaceWith(boxHTML.text());
            plainTags = jQuery('#image-tag-plain-' + safeId).replaceWith(titleHTML.text());
        } else {
            // Create a new tag-link box and turn it into draggable
            ImageTags.turnDraggable(jQuery('.tag-image-wrapper').append(boxHTML.text()).children().last());
            // Create the new tag-plain link
            plainTags = jQuery('.tag-plain-tags');
            plainTags.append((plainTags.children().length > 0 ? ImageTags.hyphen : '') + titleHTML.text());
            plainTags.show().parent().find('.tag-plain-no-tag').hide();
        }
        // Modify events of newly created elements in the page
        ImageTags.turnDraggable(jQuery('#image-tag-' + safeId));
        ImageTags.preventRealLink(jQuery('#image-tag-link-plain-' + safeId));
        ImageTags.turnEditable(jQuery('#image-tag-plain-' + safeId + ' .tag-edit'));
        ImageTags.turnRemovable(jQuery('#image-tag-plain-' + safeId + ' .tag-remove'));

    },
    
    onRemoveSuccess: function(data, status, request) {
        /* Called after removal success
         */

        // Get the removed box/label and remove them
        var json = eval('(' + data + ')');
        var removed = json.removed;
        jQuery.each(removed, function(pos, id) {
            var safeId = id.replace('.', '-');
            jQuery('#image-tag-' + safeId + ', #image-tag-plain-' + safeId).remove();
        });
        // Once removed, re-write tag-list with the corresponding hyphens.
        var plainTags = jQuery('.tag-plain-tags');
        var children = plainTags.children().clone(true);
        plainTags.empty();
        children.each(function(pos, el) {
            plainTags.append(el);
            if(pos<children.length-1) {
                plainTags.append(ImageTags.hyphen);
            }
        });
        // If all labels were removed, show "No tags yet" legend.
        if(children.length==0) {
            plainTags.hide().parent().find('.tag-plain-no-tag').show();

        }
    },
    
    checkRequired: function(event) {
        /* Helper method to add/remove missing-value class to fields
         */
        var field = jQuery(event.target);
        if(field.val()==='') {
            field.addClass('field-missing-value');
        } else {
            field.removeClass('field-missing-value');
        }
    },
  
    prepareEmbedOptions: function() {
        /* Turn original HTML with labels and fields
         * into more fancy radio-buttons to show embed options
         */
        var code = jQuery('.tag-embed-code').removeClass('tag-embed-code').addClass('tag-embed-code-dyn');
        var labels = code.find('label').hide();
        var inputs = code.find('input').hide();
        var brs = code.find('br').remove();
        labels.each( function(idx, val) {
            var text = jQuery(val).text();
            code.find('dd').prepend('<label for="tag-embed-label-' + text + '"><input type="radio" class="radio" name="tag-embed-choice" id="tag-embed-label-' + text + '" value="' + text + '"/>' + text + '</label>');
        });
        code.find('input[type=radio]').click(function(event) {
            code.find('.tag-embed-code-selected').hide();
            code.find('#' + event.target.id.replace('-label-', '-code-')).show().addClass('tag-embed-code-selected').select();
        }).first().click();

    }
    
};

// Finally, add all backed up methods and attributes to the new ImageTags object
for(var fn in ImageTags_bak) {
    ImageTags[fn] = ImageTags_bak[fn];
}

// and delete the backed up ImageTags
delete window['ImageTags_bak']
