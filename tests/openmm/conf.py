# -*- coding: utf-8 -*-

import os
import sys
import tarfile

extensions = ['sphinx.ext.mathjax', 'sphinx.ext.ifconfig', 'sphinxcontrib.autodoc_doxygen']

autosummary_generate = True
autodoc_default_flags = ['members', 'inherited-members']
autodoc_member_order = 'bysource'

source_suffix = '.rst'
master_doc = 'index'

project = u'OpenMM'
copyright = u'2015, Stanford University and the Authors'

exclude_patterns = ['_build', 'autodoc_doxygen']
html_static_path = ['_static']
templates_path = ['_templates']

pygments_style = 'sphinx'

html_theme = "alabaster"
html_theme_options = {
    'description': "High performance molecular simulation on GPUs",
    'github_button': False,
    'logo_name': False,
    'logo': 'logo.png',
}

html_sidebars = {
    '**': [
        'about.html',
        'searchbox.html',
        'navigation.html',
    ]
}


with tarfile.open(os.path.join(os.path.dirname(__file__), '..', 'openmm-doxygen-xml.tar.bz2'), "r:bz2") as f:
    f.extractall()

doxygen_xml = os.path.join(os.path.dirname(__file__), "xml")
