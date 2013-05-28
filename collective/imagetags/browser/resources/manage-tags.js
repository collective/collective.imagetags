/* collective.imagetags JavaScript for managing tagged images */

jQuery(document).ready(function() {
    if(jQuery('.tag-image-wrapper').length) {
        // Mark management screen as inline managing
        jQuery('.tag-manage').removeClass('tag-manage').addClass('tag-manage-inline');
        // Hide table of tags management; 'Tag details' fieldset; and ajax-form div, containing the very form
        jQuery('#imagetags-manage, #imagetags-form, #ajax-form').hide();
        // Hide x, y fields
        jQuery('#form-widgets-x, #form-widgets-y').each(function(idx, el) {
            jQuery(el).closest('div.field').hide();
        });
        jQuery('#tag-start-tagging').show().click(ImageTags.startTagging);
        jQuery('#tag-stop-tagging').click(ImageTags.stopTagging);
        // Remove unload protection from forms (taken from formUnload.js)
        var tool = window.onbeforeunload && window.onbeforeunload.tool;
        if (tool) {
            try {
                tool.removeForms.apply(tool, jQuery('form.enableUnloadProtection').get());
            } catch(err) {
                // do nothing
            }
        }
        // auto-select input fields
        jQuery('.tag-embed-code input').focus(function(event) {event.target.select();});
        ImageTags.prepareEmbedOptions();
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
    draggableConfig: {revert: false, cancel: 'span.tag-link-title'},
    initiated: false,
    
    initTagging: function() {
        /* Initial setup that doesn't need to be done again
         */
        // Find the form and bind its "onsubmit" event
        var formContainer = jQuery('#ajax-form');
        var form = formContainer.find('form');
        form.submit(ImageTags.submitForm);
        // Add keyup event to required fields
        form.find('input.required').keyup(ImageTags.checkRequired);    
        // Hide save button and allow multi submit
        form.find('input.submit-widget').hide().addClass('allowMultiSubmit');
        ImageTags.draggableConfig['stop'] = ImageTags.onBoxStopDragging;
        ImageTags.draggableConfig['start'] = ImageTags.onBoxStartDragging;
        ImageTags.initiated = true;
    },

    startTagging: function(event) {
        /* When "Start tagging" link is pressed, perform the following actions
         */
        if(event) {
            event.preventDefault();
            event.stopPropagation();
        }
        // Hide #tag-start link and show tag-stop link
        jQuery('#tag-start-tagging').hide();
        jQuery('html, body').animate({scrollTop: jQuery('#tag-stop-tagging-box').show().offset().top-10}, 1000);
        if(!ImageTags.initiated) {
            ImageTags.initTagging();
        }

        // Add a special tag-tagging class and bind click event on the wrapper
        jQuery('.tag-image-wrapper').addClass('tag-tagging').click(ImageTags.onWrapperClick);
        // Turns boxes (a.tag-link) into draggable, bind the stop event and add a special class to them
        ImageTags.turnDraggable(jQuery('.tag-image-wrapper a.tag-link'));
        // Create helper action links in tag-tagging box
        ImageTags.createActionLinks(jQuery('.tag-link-plain'));
        // Add a special tag-tagging class to the a.tag-plain links
        jQuery('.tag-tag-list').addClass('tag-tagging');
        // Bind click event to a.tag-edit links
        ImageTags.turnEditable(jQuery('.tag-edit'));
        // Create a 'confirm remove' box
        jQuery('body').after('<div style="display: none; " id="imagetags-confirm-remove">' + ImageTagsLabels.removeConfirmText + '</div>');
        // Bind click event to a.tag-remove links
        ImageTags.turnRemovable(jQuery('.tag-remove, .tag-cross'));
        // Bind hover event to a.tag-cross to provide hover effect
        jQuery('.tag-cross').hover(function() {
            jQuery(this).addClass('ui-state-active');
        }, function() {
            jQuery(this).removeClass('ui-state-active');
        });
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
        jQuery('#tag-stop-tagging-box').fadeOut();
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
    
    contextUrl: function() {
        /* Calculates the objects URL
        */
        var url = document.location.href;
        if(url.indexOf('?')>-1) {
            url = url.substring(0, url.indexOf('?'));
        }
        return url;

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
    
    createActionLinks: function(collection) {
        var url = ImageTags.contextUrl();
        collection.each(function(idx, el) {
            var id = el.id.replace('image-tag-link-plain-', '');
            // If editLink exists, we don't need to create it again
            var editLink = jQuery('#image-tag-edit-' + id);
            if(editLink.length===0) {
                var buffer = [];
                buffer.push(' <span class="tag-actions">(');
                buffer.push('<a class="tag-remove" href="' + url + '?form.widgets.remove:list=' + id + '&ajax:int=1">' + ImageTagsLabels.removeLinkText + '</a>');
                buffer.push(' | ');
                buffer.push('<a class="tag-edit" id="image-tag-edit-' + id + '" href="' + url + '?id=' + id + '">' + ImageTagsLabels.editLinkText + '</a>');
                buffer.push(')</span>');
                jQuery(el).after(buffer.join('\n'));
                // We also create an icon-link inside the tag-link
                jQuery('#image-tag-' + id).append('<a class="tag-cross ui-state-default" href="' + url + '?form.widgets.remove:list=' + id + '&ajax:int=1" title="' + ImageTagsLabels.removeLinkText + '"><span class="ui-icon ui-icon-closethick">' + ImageTagsLabels.removeLinkText + '</span></a>');
            }
        });
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
        var finalPosition = {};
        if(newX<0) {
            newX = -box.width()/2;
            finalPosition['left'] = newX + 'px';
        }
        if(newX>wWidth) {
            newX = (wWidth - box.width()/2);
            finalPosition['left'] = newX + 'px';
        }
        if(newY>wHeight) {
            newY = (wHeight - box.height()/2);
            finalPosition['top'] = newY + 'px';
        }
        if(newY<0) {
            newY = -box.height()/2;
            finalPosition['top'] = newY + 'px';
        }
        // If "desired" position is out of limits, re-place the box
        if(finalPosition['top'] !== undefined || finalPosition['left'] !== undefined) {
            box.animate(finalPosition, 'fast');
        }
        // Translate X,Y into percentages
        var perX = Math.min(100, Math.max(0, (newX/wWidth*100).toFixed(1)));
        var perY = Math.min(100, Math.max(0, (newY/wHeight*100).toFixed(1)));
        // Prepare data to be sent to server
        var id = box.attr('id').replace('image-tag-', '');
        var title = box.find('.tag-link-title').text();
        var url = box.attr('href') || '';
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
        ImageTags.hideForm();
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
        wrapper.find('.tag-link-active').removeClass('tag-link-active');
        var wWidth = wrapper.width();
        var wHeight = wrapper.height();
        var position = box.position();
        var newX = position.left /*- offsetW.left*/ + box.width()/2;
        var newY = position.top /*- offsetW.top*/ + box.height()/2;
        // Translate X,Y into percentages
        var perX = Math.min(100, Math.max(0, (newX/wWidth*100).toFixed(1)));
        var perY = Math.min(100, Math.max(0, (newY/wHeight*100).toFixed(1)));
        // Pre-load data on the form
        var id = box.attr('id').replace('image-tag-', '');
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
        // Set removeLink href to confirmDiv data. This is because of some issue with jquery 1.3.2 (Plone 3)
        var link = jQuery(event.target).closest('a');
        confirmDiv.data('removeLinkURL', link.attr('href'));
        
        var buttons = {};
        buttons[ImageTagsLabels.noButtonText] = function() {
            jQuery(this).dialog('close');
        };
        buttons[ImageTagsLabels.yesButtonText] = function() {
            jQuery(this).dialog('close');
            var confirmDiv = jQuery('#imagetags-confirm-remove')
            var removeLinkURL = confirmDiv.data('removeLinkURL');
            confirmDiv.data('removeLinkURL', null)
            jQuery.get(removeLinkURL, ImageTags.onRemoveSuccess);
        };
        // Separate dialog open in two lines due to some issue with jquery-ui 1.7.2 (Plone 3)
        confirmDiv.dialog({
            autoOpen: false,
            title: ImageTagsLabels.removeLinkText,
            resizable: false,
            buttons: buttons,
            modal: true
        });
        confirmDiv.dialog('open');
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
            if(field=='x' || field=='y') {
                value = ImageTags.replaceDecimalSeparator(value);
            }
            if(field=='url') {
                value = value=='#' ? '' : value;
            }
            form.find('input[name=' + prefix + field + ']').val(value);
        });
    },
    
    hideForm: function() {
        /* Reset and hide tag details form
         */
        var formContainer = jQuery('#ajax-form');
        ImageTags.resetForm();
        formContainer.dialog('close');         
    },

    showForm: function(box) {
        /* Display the edit tag details form
         */
        var formContainer = jQuery('#ajax-form');
        // Display the form dialog
        buttons = {};
        buttons[ImageTagsLabels.saveButtonText] = ImageTags.submitForm;
        // Separate dialog open in two lines due to some issue with jquery-ui 1.7.2 (Plone 3)
        formContainer.dialog({
            title: ImageTagsLabels.tagFormTitle, 
            resizable: false,
            open: function(event, ui) {
                jQuery(this).find('input[type!=hidden]:first').focus();
            },
            buttons: buttons
        });
        // onclose function. It gets the box as extra data to remove a css class name
        var onclose = function(event, ui) {
            ImageTags.resetForm();
            if(event.data && event.data[0]) {
                var box = jQuery(event.data[0]);
                box.removeClass('tag-link-active');
            }
        };
        formContainer.bind('dialogclose', box, onclose);
        formContainer.dialog('open');
        
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
        jQuery.post(form.attr('action'), form.serialize() + '&ajax:int=1&' + button.name + '=' + button.value, onPostSuccess);
    },
    
    resetForm: function() {
        /* Reset the form to empty values (except for the "field"-named field)
         */
        var container = jQuery('#ajax-form');
        container.find('input[type!=submit],select,textarea').not('input[name$=field:list],input[name$=ajax],input[name$=decimal]').val('');
        container.find('.field-missing-value').removeClass('field-missing-value');
    },

    onPostSuccess: function(data, status, request) {
        /* Called after submission success
         */
        // Close (and reset) the form
        jQuery('#ajax-form').dialog('close');
        ImageTags.resetForm();
        // Take the response data and show/update boxes or tags
        var root = request ? jQuery(request.responseXML.documentElement) : jQuery(data.documentElement);
        var id = root.attr('id');
        var boxHTML = root.find('box');
        var titleHTML = root.find('title');
        var box = jQuery('#image-tag-' + id);
        var plainTags;
        if(box.length>0) {
            box.replaceWith(boxHTML.text());
            plainTags = jQuery('#image-tag-plain-' + id).replaceWith(titleHTML.text());
        } else {
            // Create a new tag-link box and turn it into draggable
            jQuery('.tag-image-wrapper').append(boxHTML.text());
            // Create the new tag-plain link
            plainTags = jQuery('.tag-plain-tags');
            plainTags.append((plainTags.children().length > 0 ? '<span class="tag-hyphen">' + ImageTagsLabels.hyphenLabel + '</span>': '') + titleHTML.text());
            plainTags.show().parent().find('.tag-plain-no-tag').hide();
        }
        // Modify events of newly created elements in the page
        ImageTags.turnDraggable(jQuery('#image-tag-' + id));
        ImageTags.preventRealLink(jQuery('#image-tag-link-plain-' + id));
        ImageTags.createActionLinks(jQuery('#image-tag-link-plain-' + id));
        ImageTags.turnEditable(jQuery('#image-tag-plain-' + id + ' .tag-edit'));
        ImageTags.turnRemovable(jQuery('#image-tag-plain-' + id + ' .tag-remove'));
        var cross = jQuery('#image-tag-' + id + ' .tag-cross');
        ImageTags.turnRemovable(cross);
        // Bind hover event to a.tag-cross to provide hover effect
        cross.hover(function() {
            jQuery(this).addClass('ui-state-active');
        }, function() {
            jQuery(this).removeClass('ui-state-active');
        });
        

    },
    
    onRemoveSuccess: function(data, status, request) {
        /* Called after removal success
         */

        // Get the removed box/label and remove them (together with corresponding hyphens)
        var json = data.removed ? data : eval('(' + data + ')');
        var removed = json.removed;
        jQuery.each(removed, function(pos, id) {
            jQuery('#image-tag-' + id).remove();
            var plainTag = jQuery('#image-tag-plain-' + id);
            if(plainTag.prev().length===0) {
                plainTag.next().remove();
            } else {
                plainTag.prev().remove();
            }
            plainTag.remove();
        });
        var plainTags = jQuery('.tag-plain-tags');
        // If all labels were removed, show "No tags yet" legend.
        if(plainTags.children().length===0) {
            plainTags.hide().parent().find('.tag-plain-no-tag').show();

        }
    },
    
    replaceDecimalSeparator: function(number) {
        // Replace JavaScript number decimal separator with server expected decimal separator
        var separator = ImageTagsLabels.decimalSeparator;
        if(separator!='.') {
            return number.toString().replace('.', separator);
        } else {
            return number;
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
        var dd = code.find('dd');
        var labels = code.find('label').hide();
        code.find('input').hide();
        code.find('br').remove();
        labels.each( function(idx, val) {
            var text = jQuery(val).text();
            dd.prepend('<label for="tag-embed-label-' + text + '"><input type="radio" class="radio" name="tag-embed-choice" id="tag-embed-label-' + text + '" value="' + text + '"/>' + text + '</label>');
        });
        // Create a textarea to display embed code
        dd.append('<textarea id="tag-embed-textarea"></textarea>').find('#tag-embed-textarea').click(function(event) {
            event.target.select();
        });
        // When clicking radio buttons, replace textarea value with matching hidden input fields
        code.find('input[type=radio]').click(function(event) {
            jQuery('#tag-embed-textarea').attr('value', code.find('#' + event.target.id.replace('-label-', '-code-')).attr('value')).select();
        });
        // Pre-select first option
        code.find('input[type=radio]:first').click();
    }
    
};

// Finally, add all backed up methods and attributes to the new ImageTags object
for(var fn in ImageTags_bak) {
    ImageTags[fn] = ImageTags_bak[fn];
}

// and delete the backed up ImageTags
if(window['ImageTags_bak']) {
    delete window['ImageTags_bak'];
}
