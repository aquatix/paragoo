"""
paragoo plugin for loading tiles
"""
import os


class TileNotFoundException(Exception):
    pass


def render(site_path, params):
    """
    Look up the tile file from site import import config in site_path
    Format of params: <key>
    """
    if os.path.isfile(site_path, 'tiles', params[0] + '.desc'):
        return 'found'
    else:
        raise NewsNotFoundException(params[0])
