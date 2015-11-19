import inspect
from lxml import etree as ET

from sphinx import addnodes
from docutils import nodes
from docutils.statemachine import ViewList
from sphinx.ext.autosummary import Autosummary, autosummary_table

from . import get_doxygen_root
from .autodoc import DoxygenMethodDocumenter



def import_by_name(name, prefixes=[None]):
    env = inspect.stack()[1].frame.f_locals['env']
    parent = str(env.ref_context.get('cpp:parent')[0])

    xpath_query = ('.//compoundname[text()="%s"]/../'
           'sectiondef[@kind="public-func"]/memberdef[@kind="function"]/'
           'name[text()="%s"]/..') % (parent, name)
    obj = get_doxygen_root().xpath(xpath_query)[0]
    full_name = parent + '.' + name
    out = (full_name, obj, full_name, '')
    return out


def get_documenter(obj, parent_or_full_name):
    if not ET.iselement(obj):
        return setup.autosummary_get_documenter(obj, parent_or_full_name)

    full_name = parent_or_full_name
    if obj.tag == 'memberdef':
        def creator(directive, _):
            return DoxygenMethodDocumenter(directive, full_name)
        return creator
    else:
        raise NotImplementedError()


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
            real_name = name
            qualifier = 'cpp:any'
            #if 'nosignatures' not in self.options:
            #    col1 = ':%s:`%s <%s>`\ %s' % (qualifier, name, real_name, sig)
            #else:
            col1 = ':%s:`%s <%s>`' % (qualifier, name, real_name)

            print(col1)
            col2 = summary
            append_row(col1, col2)

        return [table_spec, table]

    # def get_table(self, items):
    #     table_spec, table = super(DoxygenAutosummary, self).get_table(items)
    #
    #     rows =  table.children[0].children[0].children[2]
    #     for row in rows:
    #
    #
    #         text = 'sdfds'
    #
    #
    #         node = nodes.paragraph('')
    #         vl = ViewList()
    #         vl.append(text, '<autosummary>')
    #
    #         import IPython as ip
    #         ip.embed()
    #
    #         col1 = rows[0].replace(node)
    #
    #
    #     return [table_spec, table]
