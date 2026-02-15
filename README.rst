⚠️  `Moved to Codeberg <https://codeberg.org/diginaut/paragoo>`_ | `Read here why <https://dammit.nl/jumping-the-github-ship.html>`_ ⚠️

Be sure to check it out over there, as the rewrite with lots of fixes and updates will not be published here.

**This repository is not mirrored.**


paragoo
=======

|PyPI version| |PyPI license| |Code health| |Codacy|

`paragoo`_ is a static site generator, written in Python. It takes a
simple `yaml`_ file with the structure of the site, the source
Markdown/HTML content files and the `Jinja2`_ based templates and builds
a directory structure with the final website.

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


What's new?
-----------

See the `Changelog`_.


.. _paragoo: https://github.com/aquatix/paragoo
.. _yaml: https://en.wikipedia.org/wiki/YAML
.. _Jinja2: http://jinja.pocoo.org/
.. |PyPI version| image:: https://img.shields.io/pypi/v/paragoo.svg
   :target: https://pypi.python.org/pypi/paragoo/
.. |PyPI license| image:: https://img.shields.io/github/license/aquatix/paragoo.svg
   :target: https://pypi.python.org/pypi/paragoo/
.. |Code health| image:: https://landscape.io/github/aquatix/paragoo/master/landscape.svg?style=flat
   :target: https://landscape.io/github/aquatix/paragoo/master
   :alt: Code Health
.. |Codacy| image:: https://api.codacy.com/project/badge/Grade/7fff3d151d3c4ab087b22b8e04a008fe
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/aquatix/paragoo?utm_source=github.com&utm_medium=referral&utm_content=aquatix/paragoo&utm_campaign=badger
.. _paragoo material theme: https://github.com/aquatix/paragoo-theme-material
.. _Changelog: https://github.com/aquatix/paragoo/blob/master/CHANGELOG.md
