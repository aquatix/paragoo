import os
import sys
from jinja2 import Template
import jinja2
import yaml
import click
import settings

## Main program
@click.group()
def cli():
    """
    Paragoo website generator
    """
    pass


@cli.command()
@click.option('-c', '--config', prompt='Site config path')
def check_config(config):
    """
    Check site config (site.yaml) for correctness
    """
    click.secho('Needs implementing', fg='red')


#@cli.command('run_disruptions')
@cli.command()
@click.option('-s', '--site', prompt='Site path')
@click.option('-t', '--template', prompt='Template path')
def generate_site(site, template):
    """
    Generate the website specified in the config
    """

    # Templates can live anywhere, define them in settings.py
    try:
        f = open(os.path.join(site, 'site.yaml'))

        print('Reading structure from ' + os.path.join(site, 'site.yaml'))

        structure = yaml.safe_load(f)
        f.close()
    except IOError as e:
        print e
        sys.exit(1)

    print structure

    # Templates can live anywhere, define them in settings.py
    template_dir = settings.template_path
    #loader = jinja2.FileSystemLoader(template_dir)
    loader = jinja2.FileSystemLoader(
            [template_dir,
             os.path.join(os.path.dirname(__file__), 'templates/includes'),
             os.path.join(os.path.dirname(__file__), 'templates')])
    environment = jinja2.Environment(loader=loader)

    template = environment.get_template('base.html')

    for section in structure:
        # loop over the sections
        print section
        section_data = structure[section]
        print(section_data['name'])
        for page in section_data:
            # loop over its pages
            print(page)

    #template = Template('Hello {{ name }}!')
    template.render(name='John Doe')


if __name__ == '__main__':
    """
    Paragoo is ran standalone
    """
    cli()
