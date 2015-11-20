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

exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = "alabaster"
html_theme_options = {
    'description': "Test site",
    'github_button': False,
}

html_sidebars = {
    '**': [
        'about.html',
        'searchbox.html',
        'navigation.html',
    ]
}

# needs to be unpacked from the included tarball
doxygen_xml = os.path.join(os.path.dirname(__file__), "..", "xml")
