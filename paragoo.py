import os
import sys
import jinja2
import yaml
import click
import markdown
import shutil
import datetime


CONTENT_TYPES = {
    'markdown': 'md',
    'html': 'html',
    'gallery': 'gallery',
}


def generate_navbar(structure):
    navbar = []
    for section in structure['sections']:
        section_data = structure['sections'][section]
        if not 'pages' in section_data:
            print ' -  section ' + section + ' does not have pages'
            url = '/' + section + '/'
            title = section_data['title']
            navbar.append((url, section, title))
        else:
            for page in section_data['pages']:
                url = '/' + section + '/' + page
                title = structure['sections'][section]['pages'][page]['title']
                #navbar.append(structure['sections'][section]['pages'][page])
                navbar.append((url, page, title))
    print navbar
    return navbar


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def get_file_contents(filename):
    data = None
    try:
        with open(filename) as pf:
            data = pf.read()
    except IOError:
        #print 'File not found: ' + filename
        pass
    return data


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
            data = get_file_contents(try_filename)
            if data:
                print ' r  ' + try_filename
                break
    else:
        filename += '.' + CONTENT_TYPES[content_type]
        print ' r  ' + filename
        data = get_file_contents(filename)
    if data and content_type == 'markdown':
        data = markdown.markdown(data, output_format='html5')
    return data


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
@click.option('--clean/--noclean', help='Clean the output_dir first or not', default=False)
def generate_site(site, template, output_dir, clean):
    """
    Generate the website specified in the config
    """
    try:
        f = open(os.path.join(site, 'site.yaml'))

        print(' r  Reading structure from ' + os.path.join(site, 'site.yaml'))

        structure = yaml.safe_load(f)
        f.close()
    except IOError as e:
        print e
        sys.exit(1)

    print structure

    # Templates can live anywhere, define them on the command line
    template_dir = template
    #loader = jinja2.FileSystemLoader(template_dir)
    loader = jinja2.FileSystemLoader(
            [template_dir,
             os.path.join(os.path.dirname(__file__), 'templates/includes'),
             os.path.join(os.path.dirname(__file__), 'templates')])
    environment = jinja2.Environment(loader=loader)

    template = environment.get_template('base.html')

    if clean:
        print ' d  Cleaning up output_dir ' + output_dir
        if os.path.exists(output_dir):
            current_time = datetime.datetime.now()
            dt_format = '%Y-%m-%dT%H:%M:%S%z'
            timestamp = current_time.strftime(dt_format)
            #dst = os.path.join(os.path.dirname(output_dir), timestamp)
            dst = output_dir + '_' + timestamp
            shutil.move(output_dir, dst)
    else:
        print '[!] Not cleaning up, overwrite existing, keeping others'

    ensure_dir(output_dir)

    # Site-global texts
    site_fields = ['title', 'author', 'description', 'copyright', 'footer']
    site_data = {}
    for field in site_fields:
        site_data[field] = structure[field]

    source_uses_subdirs = True
    try:
        source_uses_subdirs = structure['subdirs']
    except KeyError:
        print 'Defaulting to searching sub directories for source files'

    # Create navbar datastructure
    navbar = generate_navbar(structure)

    for section in structure['sections']:
        # Iterate over the sections
        section_data = structure['sections'][section]
        section_filename = os.path.join(output_dir, section)
        source_section_filename = os.path.join(site, section)
        if not source_uses_subdirs:
            source_section_filename = os.path.join(site, 'pages', section)
        #print section_filename
        if not 'pages' in section_data:
            print ' -  section ' + section + ' does not have pages'
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
                data['htmlbody'] = htmlbody
                data['navbar'] = navbar
                data['active_page'] = section
                data['structure'] = structure
                # Render the page
                output = template.render(data)
                filename = os.path.join(section_filename, 'index.html')
                ensure_dir(filename)
                print ' w  ' + filename
                with open(filename, 'w') as pf:
                    pf.write(output)
            else:
                print '[E] hm, also no section page found'
        else:
            very_first_page = True # Homepage of website, root
            first_page = True # Homepage of section
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
                data['page'] = page_data
                data['htmlbody'] = htmlbody
                data['navbar'] = navbar
                data['active_page'] = page
                data['structure'] = structure
                # Render the page
                output = template.render(data)
                # Save to output_dir
                filename = os.path.join(section_filename, page, 'index.html')
                print ' w  ' + filename
                ensure_dir(filename)
                with open(filename, 'w') as pf:
                    pf.write(output)
                if first_page:
                    # Also save an index file for the section (first page in section is section homepage)
                    first_page = False
                    filename = os.path.join(section_filename, 'index.html')
                    print ' w  ' + filename
                    with open(filename, 'w') as pf:
                        pf.write(output)
                if very_first_page:
                    # Also save an index file for the homepage, root of site
                    very_first_page = False
                    filename = os.path.join(output_dir, 'index.html')
                    print ' w  ' + filename
                    with open(filename, 'w') as pf:
                        pf.write(output)
    static_dirs = ['images', 'styles', 'scripts']
    for dirname in static_dirs:
        print ' -  copying directory "' + dirname + '"'
        #src = os.path.join(template_dir, dirname)
        src = os.path.join(os.path.dirname(site), dirname)
        dst = os.path.join(output_dir, dirname)
        if not os.path.exists(src):
            print '[E] Source directory not found, skipping'
        else:
            try:
                shutil.copytree(src, dst, symlinks=False, ignore=None)
            except OSError:
                print '[E] Directory already exists, skipping'
    print ' -  done'


if __name__ == '__main__':
    """
    Paragoo is ran standalone
    """
    cli()
