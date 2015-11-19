class NodeVisitor(object):
    def visit(self, node):
        """Visit a node. The default implementation calls the method called
        self.visit_classname where classname is the name of the node class,
        or generic_visit() if that method doesn’t exist
        """
        method = 'visit_' + node.tag
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """This visitor calls visit() on all children of the node.

        Note that child nodes of nodes that have a custom visitor method won’t
        be visited unless the visitor calls generic_visit() or visits them itself.
        """
        for child in node.getchildren():
            self.visit(child)
        return self


class DoxygenNodeVisitor(NodeVisitor):
    def __init__(self):
        self.lines = ['']
        self.continue_line = False

    def visit_ref(self, node):
        self.lines[-1] += ':cpp:any:`%s`%s' % (node.text, node.tail)

    def visit_para(self, node):
        if node.text is not None:
            if self.continue_line:
                self.lines[-1] += node.text
            else:
                self.lines.append(node.text)
        self.generic_visit(node)
        self.lines.append('')
        self.continue_line = False

    def visit_parametername(self, node):
        ptype = None
        type_search = node.xpath('./ancestor::memberdef/param/declname[text()="%s"]/../type' % node.text)
        if type_search is not None:
            ptype = type_search[0].text

        self.lines.append((':param %s: ' % node.text) + ('(%s) ' % ptype if ptype else ''))
        self.continue_line = True

    def visit_simplesect(self, node):
        if node.get('kind') == 'return':
            self.lines.append(':returns: ')
            self.continue_line = True
        self.generic_visit(node)

    def visit_listitem(self, node):
        self.lines.append('   - ')
        self.continue_line = True
        self.generic_visit(node)

    def visit_preformatted(self, node):
        segment = [node.text]
        for n in node.getchildren():
            segment.append(n.text)
            if n.tail is not None:
                segment.append(n.tail)

        lines = ''.join(segment).split('\n')
        self.lines.extend(('.. code-block:: C++', ''))
        self.lines.extend(['  ' + l for l in lines])
