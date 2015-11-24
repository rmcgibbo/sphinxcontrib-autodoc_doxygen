from __future__ import print_function, absolute_import, division

from lxml import etree as ET
from sphinx.ext.autodoc import Documenter, members_option
from sphinx.errors import ExtensionError

from . import get_doxygen_root
from .xmlutils import format_xml_paragraph


class DoxygenDocumenter(Documenter):
    # Variables to store the names of the object being documented. modname and fullname are redundant,
    # and objpath is always the empty list. This is inelegant, but we need to work with the superclass.

    fullname = None  # example: "OpenMM::NonbondedForce" or "OpenMM::NonbondedForce::methodName""
    modname = None   # example: "OpenMM::NonbondedForce" or "OpenMM::NonbondedForce::methodName""
    objname = None   # example: "NonbondedForce"  or "methodName"
    objpath = []     # always the empty list
    option_spec = {
        'members': members_option,
    }

    def parse_name(self):
        """Determine what module to import and what attribute to document.
        Returns True and sets *self.modname*, *self.objname*, *self.fullname*,
        if parsing and resolving was successful.
        """
        # To view the context and order in which all of these methods get called,
        # See, Documenter.generate(). That's the main "entry point" that first
        # calls parse_name(), follwed by import_object(), format_signature(),
        # add_directive_header(), and then add_content() (which calls get_doc())

        # methods in the superclass sometimes use '.' to join namespace/class
        # names with method names, and we don't want that.
        self.name = self.name.replace('.', '::')

        self.fullname = self.name
        self.modname = self.fullname
        self.objpath = []

        if '::' in self.name:
            parts = self.name.split('::')
            self.objname = parts[-1]
        else:
            self.objname = self.name

        return True

    def add_directive_header(self, sig):
        """Add the directive header and options to the generated content."""
        domain = getattr(self, 'domain', 'cpp')
        directive = getattr(self, 'directivetype', self.objtype)
        name = self.format_name()
        sourcename = self.get_sourcename()
        self.add_line(u'.. %s:%s:: %s%s' % (domain, directive, name, sig),
                      sourcename)


class DoxygenClassDocumenter(DoxygenDocumenter):
    objtype = 'doxyclass'
    directivetype = 'class'
    domain = 'cpp'
    priority = 100

    option_spec = {
        'members': members_option,
    }

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        # this method is only called from Documenter.document_members
        # when a higher level documenter (module or namespace) is trying
        # to choose the appropriate documenter for each of its lower-level
        # members. Currently not implemented since we don't have a higher-level
        # doumenter like a DoxygenNamespaceDocumenter.
        return False

    def import_object(self):
        """Import the object and set it as *self.object*.  In the call sequence, this
        is executed right after parse_name(), so it can use *self.fullname*, *self.objname*,
        and *self.modname*.

        Returns True if successful, False if an error occurred.
        """
        xpath_query = './/compoundname[text()="%s"]/..' % self.fullname
        match = get_doxygen_root().xpath(xpath_query)
        if len(match) != 1:
            raise ExtensionError('[autodoc_doxygen] could not find class (fullname="%s"). I tried'
                                 'the following xpath: "%s"' % (self.fullname, xpath_query))

        self.object = match[0]
        return True

    def format_signaure(self):
        return ''

    def format_name(self):
        return self.fullname

    def get_doc(self, encoding):
        detaileddescription = self.object.find('detaileddescription')
        doc = [format_xml_paragraph(detaileddescription)]
        return doc

    def get_object_members(self, want_all):
        all_members = self.object.findall('.//sectiondef[@kind="public-func"]/memberdef[@kind="function"]')

        if want_all:
            return False, ((m.find('name').text, m) for m in all_members)
        else:
            if not self.options.members:
                return False, []
            else:
                return False, ((m.find('name').text, m) for m in all_members
                               if m.find('name').text in self.options.members)

    def filter_members(self, members, want_all):
        ret = []
        for (membername, member) in members:
            ret.append((membername, member, False))
        return ret

    def document_members(self, all_members=False):
        super(DoxygenClassDocumenter, self).document_members(all_members=all_members)
        # Uncomment to view the generated rst for the class.
        # print('\n'.join(self.directive.result))


class DoxygenMethodDocumenter(DoxygenDocumenter):
    objtype = 'doxymethod'
    directivetype = 'function'
    domain = 'cpp'
    priority = 100

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        if ET.iselement(member) and member.tag == 'memberdef' and member.get('kind') == 'function':
            return True
        return False

    def import_object(self):
        xpath_query = ('.//compoundname[text()="%s"]/../sectiondef[@kind="public-func"]'
                       '/memberdef[@kind="function"]/name[text()="%s"]/..') % tuple(self.fullname.rsplit('::',1))
        match = get_doxygen_root().xpath(xpath_query)
        if len(match) == 0:
            raise ExtensionError('[autodoc_doxygen] could not find method (modname="%s", objname="%s"). I tried '
                                 'the following xpath: "%s"' % (tuple(self.fullname.rsplit('::', 1)) + (xpath_query,)))
        self.object = match[0]
        return True

    def get_doc(self, encoding):
        detaileddescription = self.object.find('detaileddescription')
        doc = [format_xml_paragraph(detaileddescription)]
        return doc

    def format_name(self):
        # return self.object.find('definition').text
        rtype = '\n'.join(format_xml_paragraph(self.object.find('type'))).strip()
        return (rtype and (rtype + ' ') or '') + self.objname


    def format_signature(self):
        args = self.object.find('argsstring').text
        return args

    def document_members(self, all_members=False):
        pass
