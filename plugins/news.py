"""
paragoo plugin for loading news items
"""
import os


class NewsNotFoundException(Exception):
    pass


def render(site_path, environment, params):
    """
    Look up the news file from site import config in site_path
    Format of params: <key>:<offset>:<length>
    """
    filename = os.path.join(site_path, 'news', params[0] + '.desc')
    if os.path.isfile(filename):
        content = ''
        with open(filename, 'r') as f:
            content = f.readlines()
        template = environment.get_template('newsitem.html')
        print content
        items = []
        for item in content:
            parts = item.split('=')
            items.append({'key': parts[0], 'content': parts[1]})
        data = {'items': items}
        return template.render(data)
    else:
        raise NewsNotFoundException(params[0])
