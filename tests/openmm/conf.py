# -*- coding: utf-8 -*-

import os.path

extensions = ['sphinx.ext.mathjax', 'sphinx.ext.ifconfig', 'sphinxcontrib.autodoc_doxygen']

autosummary_generate = True
autodoc_member_order = 'bysource'

project="test1"
source_suffix = '.rst'
master_doc = 'index'

exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = "alabaster"
html_theme_options = {
    'description': "sphinx-contrib autodoc_doxygen test site",
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
