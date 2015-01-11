from jinja2 import Template
import yaml

f = open('site.yaml')

structure = yaml.safe_load(f)
f.close()

print structure


template = Template('Hello {{ name }}!')
template.render(name='John Doe')
