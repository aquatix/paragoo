paragoo
=======

`paragoo`_ is a static site generator, written in Python. It takes a
simple `yaml`_ file with the structure of the site, the source
Markdown/HTML content files and the `Jinja2`_ based templates and builds
a directory structure with the final website.

|PyPI version| |PyPI downloads| |PyPI license|

Installation
------------

From PyPI
~~~~~~~~~

Assuming you already are inside a virtualenv:

.. code-block:: bash

    pip install paragoo

From Git
~~~~~~~~

Create a new virtualenv (if you are not already in one) and install the
necessary packages:

.. code-block:: bash

    git clone https://github.com/aquatix/paragoo.git
    cd paragoo
    mkvirtualenv paragoo # or whatever project you are working on
    pip install -r requirements.txt


Usage
-----

Run ``python paragoo.py`` to get help. Typically, a command line looks
like this:

::

    python paragoo.py generate_site -s /path/to/site_config -t /path/to/site_templates -o /path/to/output_dir

A more involved command including a Secure CoPy to a remote server can
look like this:

::

    python paragoo.py generate_site --clean -s ../aquariusoft.org/site -t ../aquariusoft.org/templates -o /tmp/aqs --clean; scp -pqr /tmp/aqs/* vps01:/srv/aquariusoft.org/

    or:

    python paragoo.py generate_site --clean --cachebuster -s ../../../website/mydomain.net/site -t ../paragoo-theme-material/build/material-grey --pathprefix page --makerooturi -o /srv/mydomain.net

To see what commands are available, run paragoo with ``--help``:

::

    python paragoo.py --help

    or:

    python paragoo.py generate_site --help


Templates
---------

Some pre-made templates to go with paragoo: `paragoo material theme`_.


parawah?
--------

The name is derived from παράγω, which is Greek for ‘generate’,
‘produce’.

.. _paragoo: https://github.com/aquatix/paragoo
.. _yaml: https://en.wikipedia.org/wiki/YAML
.. _Jinja2: http://jinja.pocoo.org/
.. |PyPI version| image:: https://img.shields.io/pypi/v/paragoo.svg
   :target: https://pypi.python.org/pypi/paragoo/
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/paragoo.svg
   :target: https://pypi.python.org/pypi/paragoo/
.. |PyPI license| image:: https://img.shields.io/github/license/aquatix/paragoo.svg
   :target: https://pypi.python.org/pypi/paragoo/
.. _paragoo material theme: https://github.com/aquatix/paragoo-theme-material
