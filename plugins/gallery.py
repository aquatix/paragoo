"""
paragoo plugin for loading a gallery
"""
import os


class GalleryNotFoundException(Exception):
    pass


def render(site_path, structure, environment, params):
    """
    Look up the gallery config file from site import config in site_path
    Format of params: <key>:<offset>:<length>
    """
    if os.path.isfile(os.path.join(site_path, 'gallery', params[0] + '.desc')):
        return 'found'
    else:
        raise GalleryNotFoundException(params[0])
