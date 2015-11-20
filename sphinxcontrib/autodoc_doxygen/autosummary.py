import re

from sphinx import addnodes
from docutils import nodes
from docutils.statemachine import ViewList
from sphinx.ext.autosummary import Autosummary, autosummary_table

from . import get_doxygen_root
from .autodoc import DoxygenMethodDocumenter, DoxygenClassDocumenter


def import_by_name(name, env=None, prefixes=None):
    if prefixes is None:
        prefixes = [None]

    if env is not None:
        if env.ref_context.get('cpp:parent') is not None:
            prefixes.append(str(env.ref_context.get('cpp:parent')[0]))

    tried = []
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
    name = name.replace('.', '::')

    if '::' in name:
        xpath_query = (
            './/compoundname[text()="%s"]/../'
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


def get_documenter(obj, full_name):
    if obj.tag == 'memberdef':
        return DoxygenMethodDocumenter
    elif obj.tag == 'compounddef':
        return DoxygenClassDocumenter

    raise NotImplementedError(obj.tag)


class DoxygenAutosummary(Autosummary):
    def get_items(self, names):
        """Try to import the given names, and return a list of
        ``[(name, signature, summary_string, real_name), ...]``.
        """
        env = self.state.document.settings.env
        items = []

        for name in names:
            display_name = name
            if name.startswith('~'):
                name = name[1:]
                display_name = name.split('.')[-1]

            try:
                real_name, obj, parent, modname = import_by_name(name, env=env)
            except ImportError:
                self.warn('failed to import %s' % name)
                items.append((name, '', '', name))
                continue

            self.result = ViewList()  # initialize for each documenter
            documenter = get_documenter(obj, parent)(self, real_name)
            if not documenter.parse_name():
                self.warn('failed to parse name %s' % real_name)
                items.append((display_name, '', '', real_name))
                continue
            if not documenter.import_object():
                self.warn('failed to import object %s' % real_name)
                items.append((display_name, '', '', real_name))
                continue
            if documenter.options.members and not documenter.check_module():
                continue

            # -- Grab the signature
            sig = documenter.format_signature()

            # -- Grab the summary
            documenter.add_content(None)
            doc = list(documenter.process_doc([self.result.data]))

            while doc and not doc[0].strip():
                doc.pop(0)

            # If there's a blank line, then we can assume the first sentence /
            # paragraph has ended, so anything after shouldn't be part of the
            # summary
            for i, piece in enumerate(doc):
                if not piece.strip():
                    doc = doc[:i]
                    break

            # Try to find the "first sentence", which may span multiple lines
            m = re.search(r"^([A-Z].*?\.)(?:\s|$)", " ".join(doc).strip())
            if m:
                summary = m.group(1).strip()
            elif doc:
                summary = doc[0].strip()
            else:
                summary = ''

            items.append((display_name, sig, summary, real_name))

        return items

    def get_table(self, items):
        """Generate a proper list of table nodes for autosummary:: directive.

        *items* is a list produced by :meth:`get_items`.
        """
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
            # required for cpp autolink
            full_name = real_name.replace('.', '::')
            col1 = ':%s:`%s <%s>`' % (qualifier, name, full_name)
            col2 = summary
            append_row(col1, col2)

        return [table_spec, table]
