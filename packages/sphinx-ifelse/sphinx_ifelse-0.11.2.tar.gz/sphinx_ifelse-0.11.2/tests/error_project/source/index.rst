.. elif:: True

   ElifDirective without previous text shall be in the output.


Test for IfDirective
====================

Undefined element in condition
------------------------------

.. if:: a

   IfDirective /Undefined element in condition/ text shall be in the output.

Empty condition
---------------

.. if::

   IfDirective /Empty condition/ text shall not be in the output.

Test for ElIfDirective
======================

Undefined element in condition
------------------------------

.. if:: False

   ElIfDirective /Undefined element in condition/ text before shall not be in the output.

.. elif:: a

   ElIfDirective /Undefined element in condition/ text shall be in the output.

Empty condition
---------------

.. if:: False

   ElIfDirective /Empty condition/ text before shall not be in the output.

.. elif::

   ElIfDirective /Empty condition/ text shall not be in the output.


Missing IfDirective before ElIfDirective with evaluating to True
----------------------------------------------------------------

.. elif:: True

   ElIfDirective /Missing IfDirective before ElIfDirective with evaluating to True/ text shall be in the output.

Missing IfDirective before ElIfDirective with evaluating to False
-----------------------------------------------------------------

.. elif:: False

   ElIfDirective /Missing IfDirective before ElIfDirective with evaluating to False/ text shall not be in the output.

Test for ElseDirective
======================

Missing IfDirective before ElseDirective
----------------------------------------

.. else::

   ElseDirective /Missing IfDirective before ElseDirective/ text shall be in the output.
