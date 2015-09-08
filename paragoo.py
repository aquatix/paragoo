import os
import sys
from jinja2 import Template
import jinja2
import yaml
import click
import markdown


CONTENT_TYPES = {
        'markdown': 'md',
        'html': 'html',
        'gallery': 'gallery',
        }


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def load_page_source(section_dir, page, page_data):
    filename = os.path.join(section_dir, page)
    try:
        content_type = page_data['type']
    except KeyError:
        content_type = 'markdown'
    try:
        filename = page_data['file']
    except KeyError:
        print 'wtf'
    filename += '.' + CONTENT_TYPES[content_type]
    print filename
    data = None
    try:
        with open(filename) as pf:
            data = pf.read()
    except IOError:
        print 'File not found: ' + filename
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
@click.option('-s', '--site', prompt='Site path')
@click.option('-t', '--template', prompt='Template path')
@click.option('-o', '--output_dir', prompt='Output path for generated content')
@click.option('--clean/--noclean', default=False)
def generate_site(site, template, output_dir, clean):
    """
    Generate the website specified in the config
    """
    try:
        f = open(os.path.join(site, 'site.yaml'))

        print('Reading structure from ' + os.path.join(site, 'site.yaml'))

        structure = yaml.safe_load(f)
        f.close()
    except IOError as e:
        print e
        sys.exit(1)

    print structure

    try:
        # Try if output_dir is writable
        # TODO: check existence of output_dir
        # TODO: create output_dir
        f = open(os.path.join(output_dir, 'temp'), 'w')
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
    environment = jinja2.Environment(loader=loader)

    template = environment.get_template('base.html')

    if clean:
        print 'Cleaning up output_dir ' + output_dir
        # TODO: actuall clean up output_dir (danger!)
    else:
        print 'Not cleaning up, overwrite existing, keeping others'

    # Site-global texts
    site_fields = ['title', 'author', 'description', 'copyright', 'footer']
    site_data = {}
    for field in site_fields:
        site_data[field] = structure[field]

    for section in structure['sections']:
        # Iterate over the sections
        section_data = structure['sections'][section]
        section_filename = os.path.join(output_dir, section)
        source_section_filename = os.path.join(site, section)
        #print section_filename
        for page in section_data['pages']:
            # Loop over its pages
            page_data = structure['sections'][section]['pages'][page]
            htmlbody = load_page_source(source_section_filename, page, page_data)
            data = site_data.copy()
            data['site'] = site_data
            try:
                data['author'] = page_data['author']
            except KeyError:
                data['author'] = site_data['author']
            data['page'] = page_data
            data['htmlbody'] = htmlbody
            data['structure'] = structure
            output = template.render(data)
            filename = os.path.join(section_filename, page + '/index.html')
            print filename
            ensure_dir(filename)
            pf = open(filename, 'w')
            pf.write(output)
            pf.close()
    print 'done'


if __name__ == '__main__':
    """
    Paragoo is ran standalone
    """
    cli()
