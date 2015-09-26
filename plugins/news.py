"""
paragoo plugin for loading news items
"""
import os


class NewsNotFoundException(Exception):
    pass


def render(site_path, params):
    """
    Look up the news file from site import config in site_path
    Format of params: <key>:<offset>:<length>
    """
    if os.path.isfile(site_path, 'news', params[0] + '.desc'):
        return 'found'
    else:
        raise NewsNotFoundException(params[0])
