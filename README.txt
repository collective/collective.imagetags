Introduction
============
Adds a 'Tags' tab in ATContentTypes with non-empty image fields 
(News Item, Image) to allow content owners to add Text/URL tags 
(Facebook-like tags or Flickr-like notes) anchored to a certain 
position of the image.

Tagged image can then be displayed in:
 * News Items
 * Images
 * Fullscreen images
 * any other template that you want
by means of:
 * custom templates provided with this package, or
 * replacement of images via AJAX.

Showing tagged images with AJAX
-------------------------------
A special class for images is added to `TinyMCE 
<http://pypi.python.org/pypi/Products.TinyMCE>`_ and `kupu 
<http://pypi.python.org/pypi/Products.kupu>`_ settings. 
If an image with this special class "Show tags (imagetags-show)" is 
inserted in a text field it will be automatically replaced via AJAX 
to display not only the tags but also a "Tag this picture" link 
(available only for content owner).

This behavior can be disabled via "Image tags settings" configlet in 
control panel.

Showing tagged images with ``<iframes />``
------------------------------------------
'Tags' tab displays a list of several pieces of HTML code to embed the 
tagged image inside an ``<iframe />`` element.
HTML code can then be inserted inside a text field to display the tagged 
image.

This behavior can be disabled via "Image tags settings" configlet in 
control panel.

Features
========

Highlights
----------
- Degrades gracefully in non-JavaScript browsers
- All JavaScript interaction done with `jQuery 
  <http://jquery.com/>`_ and `jQueryUI 
  <http://jqueryui.com/>`_ (dialogs, draggables, etc.)
- i18n support (English, French, Dutch and Spanish translations)
- Tested in Plone 4.0.3 and Plone 3.3.5
- Collage view layout provided with `collective.collage.imagetags 
  <http://pypi.python.org/pypi/collective.collage.imagetags>`_

Browser support
---------------
- Linux: Firefox 3.6, Google Chrome 5.0
- Windows: Firefox 3.6, Google Chrome 5.0, Internet Explorer 7, 
  Internet Explorer 8

Known issues
============
- Content types with more than one image field are not fully 
  supported. The only missing part is to provide a way of changing 
  the tagging image in @@imagetags-manage browser view.
