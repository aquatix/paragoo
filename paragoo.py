import os
import stat
import sys
import jinja2
import yaml
import click
import markdown
import shutil
import datetime
from utilkit import fileutil
from collections import OrderedDict


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def include_type_exists(key):
    """
    Check whether the include type (plugin) is valid/exists.
    Needs a file of the format plugins/<key>.py
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.isfile(os.path.join(script_dir, 'plugins', key + '.py'))


def render_include(site, environment, key, params):
    """
    Render paragoo include. Typically looks like:
    @@@key=param@@@
    @@@key=param1:param2:param3@@@
    """
    # Load the relevant plugin
    plugin = __import__('plugins.' + key, globals(), locals(), [key], -1)
    return plugin.render(site, environment, params)


def paragoo_includes(site, environment, body, token='@@@'):
    """
    Filter that looks for blocks surrounded by `token` and include that content type in
    the rendered html
    """
    result = ''
    if body:
        body_parts = body.split(token)
        is_content = True
        for part in body_parts:
            if is_content:
                result += part
                is_content = False
            else:
                include_parts = part.split('=')
                include_params = include_parts[1].split(':')
                print '  ' + str(include_parts)
                if include_type_exists(include_parts[0]):
                    result += render_include(site, environment, include_parts[0], include_params)
                else:
                    print 'E Plugin not found for include with key "' + include_parts[0] + '"'
                is_content = True
    return result


CONTENT_TYPES = {
    'markdown': 'md',
    'html': 'html',
    'gallery': 'gallery',
}


def generate_navbar(structure, pathprefix):
    navbar = []
    for section in structure['sections']:
        navbar_section = []
        section_data = structure['sections'][section]
        section_url = os.path.join('/', pathprefix, section + '/')
        section_title = section_data['title']
        if 'pages' in section_data:
            for page in section_data['pages']:
                url = os.path.join('/', pathprefix, section, page)
                title = structure['sections'][section]['pages'][page]['title']
                if title:
                    # Only add a page to the navigation if it has a title, otherwise it's hidden
                    navbar_section.append((url, page, title))
        if section_title:
            navbar.append((section_url, section, section_title, navbar_section))
    return navbar


def load_page_source(source_uses_subdirs, section_dir, page, page_data):
    if page:
        if source_uses_subdirs:
            filename = os.path.join(section_dir, page)
        else:
            filename = section_dir + '_' + page
    else:
        # Section without pages, only one source file
        filename = section_dir

    try:
        content_type = page_data['type']
    except KeyError:
        content_type = 'unknown'
    try:
        filename = page_data['file']
    except KeyError:
        # No filename was defined explicitely (normal behaviour)
        pass
    if content_type == 'unknown':
        # Try to find the file
        for ct in CONTENT_TYPES:
            try_filename = filename + '.' + ct
            data = fileutil.get_file_contents(try_filename)
            if data:
                break
    else:
        filename += '.' + CONTENT_TYPES[content_type]
        data = fileutil.get_file_contents(filename)
    if data and content_type == 'markdown':
        data = markdown.markdown(data, output_format='html5')
    return data


def template_replace(content, replacements):
    """
    Replace text in rendered page with their replacements, for example to ensure
    absolute paths, or replace links of the type:
    href="page/section1/page1/"
    with
    href="/page/section1/page1/"
    when 'page' is pathprefix
    """
    #for key, value in replacements:
    for needle in replacements:
        content = content.replace(needle, replacements[needle])
    return content


## Main program
@click.group()
def cli():
    """
    Paragoo website generator
    """
    pass


@cli.command()
@click.option('-s', '--site', prompt='Site path')
def check_config(site):
    """
    Check site config (site.yaml) for correctness
    """
    click.secho('Needs implementing', fg='red')


#@cli.command('run_disruptions')
@cli.command()
@click.option('-s', '--site', help='Site path', prompt='Site path')
@click.option('-t', '--template', help='Template path', prompt='Template path')
@click.option('-o', '--output_dir', help='Output path for generated content', prompt='Output path for generated content')
@click.option('-p', '--pathprefix', help='Prepend navigation paths with this url-part', default='')
@click.option('--makerooturi/--nomakerooturi', help='Replace relative paths starting with pathprefix to start with a /', default=False)
@click.option('--clean/--noclean', help='Clean the output_dir first or not', default=False)
def generate_site(site, template, output_dir, pathprefix, makerooturi, clean):
    """
    Generate the website specified in the config
    """
    # Change default encoding to UTF-8
    # We need to reload sys module first, because setdefaultencoding is available
    # only at startup time
    reload(sys)
    sys.setdefaultencoding('utf-8')

    print '> start'
    try:
        f = open(os.path.join(site, 'site.yaml'))

        print('r Reading structure from ' + os.path.join(site, 'site.yaml'))

        structure = ordered_load(f, yaml.SafeLoader)
        f.close()
    except IOError as e:
        print e
        sys.exit(1)

    # Templates can live anywhere, define them on the command line
    template_dir = template
    #loader = jinja2.FileSystemLoader(template_dir)
    loader = jinja2.FileSystemLoader(
            [template_dir,
             os.path.join(os.path.dirname(__file__), 'templates/includes'),
             os.path.join(os.path.dirname(__file__), 'templates')])
    environment = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    #environment.filters['paragoo_includes'] = paragoo_includes

    template = environment.get_template('base.html')

    if clean:
        print 'd Cleaning up output_dir ' + output_dir
        fileutil.archive_if_exists(output_dir)
    else:
        print '! Not cleaning up, overwrite existing, keeping others'

    fileutil.ensure_dir_exists(output_dir)

    # Site-global texts
    site_fields = ['title', 'author', 'description', 'logo', 'copyright', 'footer', 'about_title', 'about', 'linkblocks']
    site_data = {}
    for field in site_fields:
        if field in structure:
            site_data[field] = structure[field]
        else:
            print '! site field "' + field + '" not found'

    source_uses_subdirs = True
    try:
        source_uses_subdirs = structure['subdirs']
    except KeyError:
        print 'I Defaulting to searching sub directories for source files'

    if pathprefix != '' and pathprefix[0] == '/':
        # Stip leading / from the prefix
        pathprefix = pathprefix[1:]

    try:
        template_replacements = dict(structure['replacements'])
    except KeyError:
        template_replacements = {}

    print template_replacements

    if makerooturi:
        template_replacements['href="' + pathprefix] = 'href="/' + pathprefix

    # Create navbar datastructure
    navbar = generate_navbar(structure, pathprefix)

    very_first_page = True # Homepage of website, root
    for section in structure['sections']:
        # Iterate over the sections
        section_data = structure['sections'][section]
        section_filename = os.path.join(output_dir, pathprefix, section)
        source_section_filename = os.path.join(site, section)
        if not source_uses_subdirs:
            source_section_filename = os.path.join(site, 'pages', section)
        first_page = True # Homepage of section
        if not 'pages' in section_data:
            print '- section ' + section + ' does not have pages'
            page_data = structure['sections'][section]
            htmlbody = load_page_source(source_uses_subdirs, source_section_filename, None, {})
            #data = load_page_source(source_uses_subdirs, os.path.dirname(source_section_filename), section, {})
            if htmlbody:
                # Template variables
                data = site_data.copy()
                data['site'] = site_data
                try:
                    data['author'] = page_data['author']
                except KeyError:
                    data['author'] = site_data['author']
                data['page'] = section_data
                if 'description' in section_data:
                    data['description'] = section_data['description']
                if 'show_title' in section_data:
                    data['show_title'] = section_data['show_title']
                else:
                    # Default to showing the page's title
                    data['show_title'] = True
                data['htmlbody'] = paragoo_includes(site, environment, htmlbody)
                data['navbar'] = navbar
                data['active_section'] = section
                data['active_page'] = section
                data['structure'] = structure
                # Render the page
                output = template.render(data)
                output = template_replace(output, template_replacements)
                filename = os.path.join(section_filename, 'index.html')
                fileutil.ensure_dir_exists(filename)
                with open(filename, 'w') as pf:
                    pf.write(output)
                if first_page:
                    # Also save an index file for the section (first page in section is section homepage)
                    first_page = False
                    filename = os.path.join(section_filename, 'index.html')
                    with open(filename, 'w') as pf:
                        pf.write(output)
                if very_first_page:
                    # Also save an index file for the homepage, root of site
                    very_first_page = False
                    filename = os.path.join(output_dir, 'index.html')
                    with open(filename, 'w') as pf:
                        pf.write(output)
            else:
                print 'E hm, also no section page found'
        else:
            for page in section_data['pages']:
                # Loop over its pages
                page_data = structure['sections'][section]['pages'][page]
                htmlbody = load_page_source(source_uses_subdirs, source_section_filename, page, page_data)
                # Template variables
                data = site_data.copy()
                data['site'] = site_data
                try:
                    data['author'] = page_data['author']
                except KeyError:
                    data['author'] = site_data['author']
                if 'show_title' in page_data:
                    data['show_title'] = page_data['show_title']
                else:
                    # Default to showing the page's title
                    data['show_title'] = True
                data['page'] = page_data
                data['htmlbody'] = paragoo_includes(site, environment, htmlbody)
                data['navbar'] = navbar
                data['active_section'] = section
                data['active_page'] = page
                data['structure'] = structure
                # Render the page
                output = template.render(data)
                output = template_replace(output, template_replacements)
                # Save to output_dir
                filename = os.path.join(section_filename, page, 'index.html')
                fileutil.ensure_dir_exists(filename)
                with open(filename, 'w') as pf:
                    pf.write(output)
                if first_page:
                    # Also save an index file for the section (first page in section is section homepage)
                    first_page = False
                    filename = os.path.join(section_filename, 'index.html')
                    with open(filename, 'w') as pf:
                        pf.write(output)
                if very_first_page:
                    # Also save an index file for the homepage, root of site
                    very_first_page = False
                    filename = os.path.join(output_dir, 'index.html')
                    with open(filename, 'w') as pf:
                        pf.write(output)
    # Generate static pages to be used with the httpd's error directives
    error_pages = {'404': 'Not found', '403': 'Forbidden'}
    for page in error_pages:
        data['page'] = {'title': page + ' ' + error_pages[page]}
        try:
            data['htmlbody'] = paragoo_includes(site, environment, structure['errorpage'])
        except KeyError:
            data['htmlbody'] = 'An error occurred. Use the navigation to find something else on the website or use history back to go back to where you came from.'
        output = template.render(data)
        filename = os.path.join(output_dir, page + '.html')
        with open(filename, 'w') as pf:
            pf.write(output)
    # Copy the directories with static assets
    static_dirs = ['images', 'styles', 'scripts', 'css', 'font', 'js', 'static']
    src_dirs = [template_dir, os.path.dirname(site)]
    for dirname in static_dirs:
        for src_dir in src_dirs:
            src = os.path.join(src_dir, dirname)
            print '- copying directory "' + src + '"'
            dst = os.path.join(output_dir, dirname)
            if not os.path.exists(src):
                print 'E Source directory not found, skipping'
            else:
                fileutil.copytree(src, dst)
                #try:
                #    shutil.copytree(src, dst, symlinks=False, ignore=None)
                #except OSError:
                #    print 'E Directory already exists, skipping'
    print '> done'


if __name__ == '__main__':
    """
    Paragoo is ran standalone
    """
    cli()
