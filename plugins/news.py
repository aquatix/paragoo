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
        first = 1
        last = len(content)
        if len(params) == 2:
            first = int(params[1])
        if len(params) == 3:
            first = int(params[1])
            last = int(params[2])
        template = environment.get_template('news.html')
        items = []
        counter = 1
        for item in content:
            if item.strip() and first <= counter <= last:
                parts = item.split('=')
                key = parts[0]
                if key[0] == '#':
                    # Skip this entry
                    continue
                del parts[0]
                content = '='.join(parts) # content may/will contain ='s
                content = content.replace('\\n', '\n')
                items.append({'key': key.strip(), 'content': content.strip()})
                counter += 1
            elif item.strip():
                # Only count non-empty lines
                counter += 1
        data = {'items': items}
        return template.render(data)
    raise NewsNotFoundException(params[0])
