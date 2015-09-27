paragoo
-------

paragoo is a static site generator, written in Python. It takes a simple [yaml]() file with the structure of the site, the source Markdown/HTML content files and the [Jinja2]() based templates and builds a directory structure with the final website.

## Usage

Run `python paragoo.py` to get help. Typically, a command line looks like this:

```
python paragoo.py generate_site -s /path/to/site_config -t /path/to/site_templates -o /path/to/output_dir
```

A more involved command including a Secure CoPy to a remote server can look like this:

```
python paragoo.py generate_site -s ../aquariusoft.org/site -t ../aquariusoft.org/templates -o /tmp/aqs --clean; scp -pqr /tmp/aqs/* vps01:/srv/aquariusoft.org/
```

## parawah?

The name is derived from παράγω, which is Greek for 'generate', 'produce'.
