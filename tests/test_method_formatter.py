from mock import Mock
from contextlib import contextmanager

import lxml.etree as ET
from sphinxcontrib.autodoc_doxygen.autodoc import (DoxygenMethodDocumenter,
                                                   AutoDirective)
import sphinxcontrib.autodoc_doxygen


@contextmanager
def set_doxygen_root(node):
    have_old_root = False
    if hasattr(sphinxcontrib.autodoc_doxygen.setup, 'DOXYGEN_ROOT'):
        old_root = sphinxcontrib.autodoc_doxygen.setup.DOXYGEN_ROOT
        have_old_root = True

    sphinxcontrib.autodoc_doxygen.setup.DOXYGEN_ROOT = node
    yield

    if have_old_root:
        sphinxcontrib.autodoc_doxygen.setup.DOXYGEN_ROOT = old_root
    else:
        delattr(sphinxcontrib.autodoc_doxygen.setup, 'DOXYGEN_ROOT')


def test_1():
    node = ET.fromstring('''
  <compounddef id="classOpenMM_1_1System" kind="class" language="C++" prot="public">
    <compoundname>OpenMM::System</compoundname>
      <sectiondef kind="public-func">
      <memberdef kind="function" id="classOpenMM_1_1System_1ade51122d3a2ff91c394af280a3d3a375" prot="public" static="no" const="yes" explicit="no" inline="no" virt="non-virtual">
        <type>const <ref refid="classOpenMM_1_1Force" kindref="compound">Force</ref> &amp;</type>
        <definition>const Force&amp; OpenMM::System::getForce</definition>
        <argsstring>(int index) const </argsstring>
        <name>getForce</name>
        <param>
          <type>int</type>
          <declname>index</declname>
        </param>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
<para>Get a const reference to one of the Forces in this <ref refid="classOpenMM_1_1System" kindref="compound">System</ref>.</para><para><parameterlist kind="param"><parameteritem>
<parameternamelist>
<parametername>index</parametername>
</parameternamelist>
<parameterdescription>
<para>the index of the <ref refid="classOpenMM_1_1Force" kindref="compound">Force</ref> to get </para></parameterdescription>
</parameteritem>
</parameterlist>
</para>        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="/Users/rmcgibbo/projects/openmm/openmmapi/include/openmm/System.h" line="200" column="1"/>
      </memberdef>
    </sectiondef>
  </compounddef>''')

    with set_doxygen_root(node):
        directive = Mock()
        documenter = DoxygenMethodDocumenter(directive, "OpenMM::System::getForce", id="classOpenMM_1_1System_1ade51122d3a2ff91c394af280a3d3a375")

        documenter.parse_name()
        documenter.import_object()
        assert documenter.format_name() == 'const Force & getForce'
        assert documenter.format_signature() == '(int index) const '
