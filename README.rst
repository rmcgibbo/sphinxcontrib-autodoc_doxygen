=============================
sphinxcontrib-autodoc_doxygen
=============================

.. image:: https://travis-ci.org/rmcgibbo/sphinxcontrib-autodoc_doxygen.svg?branch=master
    :target: https://travis-ci.org/rmcgibbo/sphinxcontrib-autodoc_doxygen

`Example Output <https://rawgit.com/rmcgibbo/sphinxcontrib-autodoc_doxygen/gh-pages/index.html>`_

This a (pre-alpha) sphinx plugin for documenting C++ projects using data drawn from Doxygen's XML. It is similar to
Breathe. However, the implementation extends ``sphinx.ext.autodoc`` and ``sphinx.ext.autosummary`` as closely as
possble.

To get started, install the package and then add and then add ``'sphinxcontrib.autodoc_doxygen'`` to the list of
extensions in your Sphinx ``conf.py`` file. Then, in ``conf.py``, set the variable `doxygen_xml` to a string
containing the path to the directory in which the doxygen XML files live.

This adds support for a couple new directives, principlally ``autodoxysummary`` and ``autodoxyclass``.

Examples
--------

::

    .. autodoxysummary::
       :toctree: generated/
       :template: doxyclass.rst

       OpenMM::CustomIntegrator
       OpenMM::CustomCompoundBondForce


::

  .. autodoxyclass:: OpenMM::CustomCompoundBondForce


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
