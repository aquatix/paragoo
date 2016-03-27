paragoo
-------

paragoo is a static site generator, written in Python. It takes a simple [yaml](https://en.wikipedia.org/wiki/YAML) file with the structure of the site, the source Markdown/HTML content files and the [Jinja2](http://jinja.pocoo.org/) based templates and builds a directory structure with the final website.

## Usage

Run `python paragoo.py` to get help. Typically, a command line looks like this:

```
python paragoo.py generate_site -s /path/to/site_config -t /path/to/site_templates -o /path/to/output_dir
```

A more involved command including a Secure CoPy to a remote server can look like this:

```
python paragoo.py generate_site --clean -s ../aquariusoft.org/site -t ../aquariusoft.org/templates -o /tmp/aqs --clean; scp -pqr /tmp/aqs/* vps01:/srv/aquariusoft.org/

or:

python paragoo.py generate_site --clean -s ../../../website/mydomain.net/site -t ../paragoo-theme-material/build/material-grey --pathprefix page --makerooturi -o /srv/mydomain.net
```

## Templates

Some pre-made templates to go with paragoo: [paragoo material theme](https://github.com/aquatix/paragoo-theme-material).

## parawah?

The name is derived from παράγω, which is Greek for 'generate', 'produce'.
