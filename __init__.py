import os
from lxml import etree as ET

def set_doxygen_xml(app):
    setup.DOXYGEN_ROOT = ET.ElementTree(ET.Element('root')).getroot()

    for file in os.listdir(app.config.doxygen_xml):
        if file.lower().endswith('xml'):
            root = ET.parse(os.path.join(app.config.doxygen_xml, file)).getroot()
            for node in root:
                setup.DOXYGEN_ROOT.append(node)


def get_doxygen_root():
    return setup.DOXYGEN_ROOT


def setup(app):
    import sphinx.ext.autosummary
    from .autodoc import DoxygenClassDocumenter, DoxygenMethodDocumenter
    from .autosummary import import_by_name, get_documenter, DoxygenAutosummary
    from .generate import process_generate_options

    app.connect("builder-inited", set_doxygen_xml)
    app.setup_extension('sphinx.ext.autodoc')
    app.setup_extension('sphinx.ext.autosummary')

    app.add_autodocumenter(DoxygenClassDocumenter)
    app.add_autodocumenter(DoxygenMethodDocumenter)
    app.add_config_value("doxygen_xml", "", True)


    setup.autosummary_import_by_name = sphinx.ext.autosummary.import_by_name
    setup.autosummary_get_documenter = sphinx.ext.autosummary.get_documenter
    setup.autosummary_process_generate_options = sphinx.ext.autosummary.process_generate_options

    sphinx.ext.autosummary.import_by_name = import_by_name
    sphinx.ext.autosummary.get_documenter = get_documenter

    # replace process_generate_options callback
    for id, cb in app._listeners['builder-inited'].items():
        if cb == sphinx.ext.autosummary.process_generate_options:
             app._listeners['builder-inited'][id] = process_generate_options

    app.add_directive('autosummary', DoxygenAutosummary)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
