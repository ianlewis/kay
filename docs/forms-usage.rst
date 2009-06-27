================
Kay forms manual
================

Overview
--------

Kay has a utility for form handling. It is placed on kay.utils.forms,
and kay.utils.forms.modelform. Here are conceptual elements for
understanding Kay's form utilities.

* Widget

  A class that corresponds to HTML representation of a field, or even
  a form, e.g. <input type="text">, <textarea> or
  <form>...</form>. This class handles rendering HTML.

* Field

  A class that is responsible for doing validation, e.g. an FloatField
  that makes sure its data is a valid float value.

* Form

  A collection of fields that knows how to validate itself and convert
  itself to a widget.

Your First Form
---------------

Let's consider a form to implement "contact me" functionality.

.. code-block:: python

  from kay.utils import forms

  class ContactForm(forms.Form):
    subject = forms.TextField(required=True, max_length=100)
    message = forms.TextField(required=True)
    sender = forms.EmailField(required=True)
    cc_myself = forms.BooleanField(required=False)

A form is composed of Field objects. In this case, our form has four
fields: subject, message, sender and cc_myself. 
