import inspect
from lxml import etree as ET

from sphinx import addnodes
from docutils import nodes
from docutils.statemachine import ViewList
from sphinx.ext.autosummary import Autosummary, autosummary_table

from . import get_doxygen_root
from .autodoc import DoxygenMethodDocumenter, DoxygenClassDocumenter


def import_by_name(name, prefixes=[None]):
    caller_locals = inspect.stack()[1].frame.f_locals
    if 'env' in caller_locals:
        env = caller_locals['env']
        if env.ref_context.get('cpp:parent') is not None:
            prefixes.append(str(env.ref_context.get('cpp:parent')[0]))

    tried = []
    name = name.replace('.', '::')
    for prefix in prefixes:
        try:
            if prefix:
                prefixed_name = '::'.join([prefix, name])
            else:
                prefixed_name = name
            return _import_by_name(prefixed_name)
        except ImportError:
            tried.append(prefixed_name)
    raise ImportError('no module named %s' % ' or '.join(tried))


def _import_by_name(name):
    root = get_doxygen_root()

    if '::' in name:
        xpath_query = ('.//compoundname[text()="%s"]/../'
               'sectiondef[@kind="public-func"]/memberdef[@kind="function"]/'
               'name[text()="%s"]/..') % tuple(name.rsplit('::', 1))

        m = root.xpath(xpath_query)
        if len(m) > 0:
            obj = m[0]
            full_name = '.'.join(name.rsplit('::', 1))
            return (full_name, obj, full_name, '')

    xpath_query = ('.//compoundname[text()="%s"]/..' % name)
    m = root.xpath(xpath_query)
    if len(m) > 0:
        obj = m[0]
        return (name, obj, name, '')

    raise ImportError()



def get_documenter(obj, parent_or_full_name):
    if not ET.iselement(obj):
        from . import setup
        return setup.autosummary_get_documenter(obj, parent_or_full_name)

    full_name = parent_or_full_name
    if obj.tag == 'memberdef':
        def creator(directive, _):
            return DoxygenMethodDocumenter(directive, full_name)
    elif obj.tag == 'compounddef':
        def creator(directive, _):
            return DoxygenClassDocumenter(directive, full_name)

    else:
        raise NotImplementedError()

    creator.objtype = DoxygenClassDocumenter.objtype
    return creator


class DoxygenAutosummary(Autosummary):

    def get_table(self, items):
        """Generate a proper list of table nodes for autosummary:: directive.

        *items* is a list produced by :meth:`get_items`.
        """
        self.options
        table_spec = addnodes.tabular_col_spec()
        table_spec['spec'] = 'll'

        table = autosummary_table('')
        real_table = nodes.table('', classes=['longtable'])
        table.append(real_table)
        group = nodes.tgroup('', cols=2)
        real_table.append(group)
        group.append(nodes.colspec('', colwidth=10))
        group.append(nodes.colspec('', colwidth=90))
        body = nodes.tbody('')
        group.append(body)

        def append_row(*column_texts):
            row = nodes.row('')
            for text in column_texts:
                node = nodes.paragraph('')
                vl = ViewList()
                vl.append(text, '<autosummary>')
                self.state.nested_parse(vl, 0, node)
                try:
                    if isinstance(node[0], nodes.paragraph):
                        node = node[0]
                except IndexError:
                    pass
                row.append(nodes.entry('', node))
            body.append(row)

        for name, sig, summary, real_name in items:
            qualifier = 'cpp:any'
            col1 = ':%s:`%s <%s>`' % (qualifier, name, real_name.replace('.', '::'))
            col2 = summary
            append_row(col1, col2)

        return [table_spec, table]
