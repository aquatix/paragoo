import os
import sys
from jinja2 import Template
import jinja2
import yaml
import click


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


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
def generate_site(site, template, output_dir):
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

    site_info = {'title': 'example'}
    for section in structure['sections']:
        # loop over the sections
        section_data = structure['sections'][section]
        section_filename = os.path.join(output_dir, section_data['slug'])
        print section_filename
        for page in section_data['pages']:
            # loop over its pages
            page_data = structure['sections'][section]['pages'][page]
            output = template.render({'site': site_info, 'page': page_data})
            #filename = os.path.join(section_filename, page_data['slug'] + '.html')
            filename = os.path.join(section_filename, page_data['slug'] + '/index.html')
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
