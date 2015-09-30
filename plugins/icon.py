"""
paragoo plugin for looking up an icon
"""
import os


class IconNotFoundException(Exception):
    pass


def render(site_path, environment, params):
    """
    Look up the gallery config file from site import config in site_path
    Format of params: <key>:<offset>:<length>
    """
    filename = os.path.join(site_path, '..', 'images', 'icons', params[0] + '.png')
    print '  ' + filename
    if os.path.isfile(filename):
        image_path = '/images/icons/' + params[0] + '.png'
        # @TODO: render with site's icon.html template
        return image_path
    else:
        raise IconNotFoundException(params[0])
