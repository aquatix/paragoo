import os
from jinja2 import Template
import jinja2
import yaml
import settings

# Templates can live anywhere, define them in settings.py
f = open(os.path.join(setting.project_path, 'site.yaml'))

print('Reading structure from ' + os.path.join(setting.project_path, 'site.yaml'))

structure = yaml.safe_load(f)
f.close()

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
