=============================
sphinxcontrib-autodoc_doxygen
=============================

.. image:: https://travis-ci.org/rmcgibbo/sphinxcontrib-autodoc_doxygen.svg?branch=master
    :target: https://travis-ci.org/rmcgibbo/sphinxcontrib-autodoc_doxygen

`Example Output <https://rawgit.com/rmcgibbo/sphinxcontrib-autodoc_doxygen/gh-pages/index.html>`_

This a (pre-alpha) extension for sphinx that to read and display Doxygen XML output. It is similar to
Breathe. The implementation extends ``sphinx.ext.autodoc`` and ``sphinx.ext.autosummary`` as closely as
possble.

Usage
-----
In your Sphinx ``conf.py`` add ``'sphinxcontrib.autodoc_doxygen'`` to the list of extensions, and set the
variable ``doxygen_xml`` to a string containing the path to the directory containing your Doxygen XML
output.

This adds the following RST directives. ::

  autodoxysummary
  autodoxyclass
  autodoxymethod
  autodoxyenum

Examples
--------

::

    .. autodoxysummary::
       :toctree: generated/
       :template: doxyclass.rst

       OpenMM::CustomIntegrator
       OpenMM::CustomCompoundBondForce

This produces the output shown `here <https://rawgit.com/rmcgibbo/sphinxcontrib-autodoc_doxygen/gh-pages/index.html>`_


Installation
------------
You can install it with pip (py27 or py33+)::

  pip install sphinxcontrib-autodoc_doxygen
  
The necessary dependences should be grabbed by ``pip``. If you have trouble getting lxml,
here are some tips:

If you use the `Anaconda <https://www.continuum.io/downloads>`_ Python
distribution, run ``conda install lxml``. With the system package manager on linux,
``sudo apt-get install python-lxml`` or ``sudo yum install python-lxml`` should do the trick.
On Windows, you may be able to download the lxml from `Christoph Gohlke's repository
<http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml>`_. On OS X, try the following long command
``brew install libxslt libxml2; LDFLAGS="-L/usr/local/opt/libxslt/lib -L/usr/local/opt/libxml2/lib" CPPFLAGS="-I/usr/local/opt/libxml2/include -I/usr/local/opt/libxslt/include" pip install lxml``. It may take a
long time (~5 minutes), but once the wheel is built, it will be cache, so you only need
to do this once, even if switch virtualenvs.
