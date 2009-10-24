=================
Utility functions
=================

.. currentmodule:: kay.utils

There are various useful functions in :mod:`kay.utils`.

.. function:: set_trace()

   Set pdb's set_trace with appropriate configuration.

.. function:: raise_on_dev()

   Raises A RuntimeError only on development environment.

.. function:: get_timezone(tzname)

   :param tzname: The name of a timezone.
   :rtype: datetime.tzinfo inplementation

