"""
paragoo plugin for loading tiles
"""
import os


class TileNotFoundException(Exception):
    pass


def render(site_path, environment, params):
    """
    Look up the tile file from site import import config in site_path
    Format of params: <key>
    """
    filename = ''
    print os.path.join(site_path, 'tiles', params[0] + '.md')
    if os.path.isfile(os.path.join(site_path, 'tiles', params[0] + '.md')):
        filename = os.path.join(site_path, 'tiles', params[0] + '.md')
    elif os.path.isfile(os.path.join(site_path, 'tiles', params[0] + '.html')):
        filename = os.path.join(site_path, 'tiles', params[0] + '.html')
    else:
        raise TileNotFoundException(params[0])
    with open(filename, 'r') as f:
        content = f.readline()
        template = environment.get_template('newsitem.html')
        return template.render(content)
