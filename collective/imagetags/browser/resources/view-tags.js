/* collective.imagetags JavaScript for viewing tagged images */

ImageTags = window['ImageTags'] || {};

/* ImageTags object with all required functions
 * 
 */
ImageTags['linksOverOut'] = function() {

    /* Get all tag-link-plain classed links and bind the mouseover/out events 
     * to add/remove tag-show class to matching box link
     */
        jQuery('.tag-link-plain').mouseout(function() {
            var other_id = this.id.replace('tag-link-plain', 'tag');
            jQuery('#' + other_id).removeClass('tag-show');
        }).mouseover(function() {
            var other_id = this.id.replace('tag-link-plain', 'tag');
            jQuery('#' + other_id).addClass('tag-show');
        });
    };
    
ImageTags['replaceImageWithTags'] = function(rule) {
    /* Get an image based on a selector (rule) and replace it
     * with a tagged image
     */
    var imgs = jQuery(rule);
    imgs.each(function(idx, img) {
        img = jQuery(img);
        var classes = img.attr('class');
        var title = img.attr('title');
        var src = img.attr('src');
        var parts = src.split('/')
        var scale_name = parts.pop();
        var url = parts.join('/') + '/@@imagetags-img?name=' + scale_name;
        
        var loader = jQuery('<div></div>').load(url, function() {
            ImageTags.showHideHints(loader);
            img.parent().replaceWith(loader.children());
            ImageTags.linksOverOut();
            // Once the image is loaded, we can re-set attributes
            var new_img = jQuery('img[src=' + src + ']');
            if(new_img) {
                new_img.attr('class', classes);
                new_img.attr('title', title);
            }
        });
    });
};

ImageTags['showHideHints'] = function(el) {
    /* Given a jQuery element (or none), add mouseover/mouseout
     * event handler to certain areas to provide tag hints
     */
    var selector = '.tag-image-wrapper'
    var wrapper = el ? jQuery(el).find(selector) : jQuery(selector);
    wrapper.hover(function() {
        $this = jQuery(this);
        if($this.hasClass('tag-tagging')) {
            return;
        }
        $this.find('a.tag-link').hide().addClass('tag-hint').fadeIn(500);
    }, function() {
        $this = jQuery(this);
        if($this.hasClass('tag-tagging')) {
            return;
        }
        $this.find('a.tag-link').fadeOut(500, function() {
            jQuery(this).removeClass('tag-hint').show();
        });
    });
};

jQuery(document).ready(function() {
    // Add over/out events to tag-labels to show/hide matching tag boxes
    ImageTags.linksOverOut();
    // Show/hide hints of tags when entering the image area
    ImageTags.showHideHints();
    // Prevent clicking on empty tag boxes
    jQuery('a.tag-no-link').live('click', function() {
        return false;
    });
});

