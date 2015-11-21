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
In your Sphinx ``conf.py` add ``'sphinxcontrib.autodoc_doxygen'`` to the list of extensions, and set the
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

  pip install git+https://github.com/rmcgibbo/sphinxcontrib-autodoc_doxygen.git

- Dependecies with Conda (cross-platform) ::

    conda install sphinx six lxml

- Dependencies with linux system package manager (e.g. with ``/usr/local/bin/python``)::

    # debian
    sudo apt-get install python-setuptools python-lxml python-sphinx python-six python-pip
    # or, for fedora
    sudo yum install python-setuptools python-lxml python-sphinx python-six python-pip

- Dependencies with Windows

  If you use windows, I receommend using conda. If not, you may be able to download the lxml dependency from
  `Christoph Gohlke's repository <http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml>`_


