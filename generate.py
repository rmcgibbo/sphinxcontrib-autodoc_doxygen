import os

from jinja2 import FileSystemLoader, TemplateNotFound
from jinja2.sandbox import SandboxedEnvironment

from sphinx.util.osutil import ensuredir
from sphinx.jinja2glue import BuiltinTemplateLoader
from sphinx.ext.autosummary.generate import find_autosummary_in_files

from .autosummary import import_by_name, get_documenter

def _simple_info(msg):
    print(msg)


def _simple_warn(msg):
    print('WARNING: ' + msg, file=sys.stderr)


def generate_autosummary_docs(sources, output_dir=None, suffix='.rst',
                              warn=_simple_warn, info=_simple_info,
                              base_path=None, builder=None, template_dir=None):

    showed_sources = list(sorted(sources))
    if len(showed_sources) > 20:
        showed_sources = showed_sources[:10] + ['...'] + showed_sources[-10:]
    info('[autosummary] generating autosummary for: %s' %
         ', '.join(showed_sources))

    if output_dir:
        info('[autosummary] writing to %s' % output_dir)

    if base_path is not None:
        sources = [os.path.join(base_path, filename) for filename in sources]

    # create our own templating environment
    template_dirs = [os.path.join(os.path.dirname(__file__), 'templates')]

    if builder is not None:
        # allow the user to override the templates
        template_loader = BuiltinTemplateLoader()
        template_loader.init(builder, dirs=template_dirs)
    else:
        if template_dir:
            template_dirs.insert(0, template_dir)
        template_loader = FileSystemLoader(template_dirs)
    template_env = SandboxedEnvironment(loader=template_loader)

    # read
    items = find_autosummary_in_files(sources)

    # keep track of new files
    new_files = []

    # write
    for name, path, template_name in sorted(set(items), key=str):
        if path is None:
            # The corresponding autosummary:: directive did not have
            # a :toctree: option
            continue

        path = output_dir or os.path.abspath(path)
        ensuredir(path)

        try:
            name, obj, parent, mod_name = import_by_name(name)
        except ImportError as e:
            warn('[autosummary] failed to import %r: %s' % (name, e))
            continue

        fn = os.path.join(path, name + suffix)

        # skip it if it exists
        if os.path.isfile(fn):
            continue

        new_files.append(fn)

        with open(fn, 'w') as f:
            doc = get_documenter(obj, parent)
            template = template_env.get_template(template_name)

            # def get_members(obj, typ, include_public=[]):
            #     items = []
            #     for name in dir(obj):
            #         try:
            #             documenter = get_documenter(safe_getattr(obj, name),
            #                                         obj)
            #         except AttributeError:
            #             continue
            #         if documenter.objtype == typ:
            #             items.append(name)
            #     public = [x for x in items
            #               if x in include_public or not x.startswith('_')]
            #     return public, items

            ns = {}

            if doc.objtype == 'module':
                raise NotImplementedError()
            elif doc.objtype == 'class':
                pass
                #ns['members'] = dir(obj)
                #ns['methods'], ns['all_methods'] = \
                #    get_members(obj, 'method', ['__init__'])
                #ns['attributes'], ns['all_attributes'] = \
                #    get_members(obj, 'attribute')

            parts = name.split('.')
            if doc.objtype in ('method', 'attribute'):
                mod_name = '.'.join(parts[:-2])
                cls_name = parts[-2]
                obj_name = '.'.join(parts[-2:])
                ns['class'] = cls_name
            else:
                mod_name, obj_name = '.'.join(parts[:-1]), parts[-1]

            ns['fullname'] = name
            ns['module'] = mod_name
            ns['objname'] = obj_name
            ns['name'] = parts[-1]

            ns['objtype'] = doc.objtype
            ns['underline'] = len(name) * '='

            print('ns', ns)

            rendered = template.render(**ns)
            f.write(rendered)

    # descend recursively to new files
    if new_files:
        generate_autosummary_docs(new_files, output_dir=output_dir,
                                  suffix=suffix, warn=warn, info=info,
                                  base_path=base_path, builder=builder,
                                  template_dir=template_dir)



def process_generate_options(app):
    genfiles = app.config.autosummary_generate

    if genfiles and not hasattr(genfiles, '__len__'):
        env = app.builder.env
        genfiles = [env.doc2path(x, base=None) for x in env.found_docs
                    if os.path.isfile(env.doc2path(x))]

    if not genfiles:
        return

    ext = app.config.source_suffix[0]
    genfiles = [genfile + (not genfile.endswith(ext) and ext or '')
                for genfile in genfiles]

    generate_autosummary_docs(genfiles, builder=app.builder,
                              warn=app.warn, info=app.info, suffix=ext,
                              base_path=app.srcdir)
