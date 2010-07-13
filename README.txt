Introduction
============
Adds a 'Tags' tab in ATContentTypes with non-empty image fields (News Item, Image) 
to allow content owners to add Text/URL tags (Facebook-like tags) anchored to a certain
position of the image.

Tagged image can then be displayed in:
* News Items
* Images
* Fullscreen images
by means of
* custom templates provided with this package, or
* replacement of images via AJAX.

Showing tagged images with AJAX
-------------------------------
A special class for images is added to TinyMCE settings. 
If an image with this special class "Show tags (imagetags-show)" is inserted ina text field
it will be automatically replaced via AJAX to display not only the tags but also a 
"Tag this picture" link (available only for content owner).

This behavior can be disabled via "Image tags settings" configlet in control panel.

Showing tagged images with <iframes />
--------------------------------------
'Tags' tab displays a list of several pieces of HTML code to embed the tagged image
inside an <iframe /> element.
HTML code can then be inserted inside a text field to display the tagged image.

This behavior can be disabled via "Image tags settings" configlet in control panel.
