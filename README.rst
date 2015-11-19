sphinxcontrib-autodoc_doxygen
=============================

This a (pre-alpha) sphinx plugin for documenting C++ projects using data drawn from Doxygen's XML. It is similar to Breathe. However, the implementation extends ``sphinx.ext.autodoc`` and ``sphinx.ext.autosummary`` as closely as possble.

To get started, install the package and then add and then add ``'sphinxcontrib.autodoc_doxygen'`` to the list of extensions in your Sphinx ``conf.py`` file. Then, in ``conf.py``, set the variable `doxygen_xml` to a string containing the path to the directory in which the doxygen XML files live.

This adds support for a couple new directives, principlally ``autodoxysummary`` and ``autodoxyclass``.

Examples
---------

::

    .. autodoxysummary::
       :toctree: generated/
       :template: doxyclass.rst

       OpenMM::CustomIntegrator
       OpenMM::CustomCompoundBondForce


::

  .. autodoxyclass:: OpenMM::CustomCompoundBondForce
