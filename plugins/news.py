"""
paragoo plugin for loading news items
"""
import os


class NewsNotFoundException(Exception):
    pass


def open_file(site_path, params):
    filename = os.path.join(site_path, 'news', params[0] + '.desc')
    if os.path.isfile(filename):
        content = ''
        with open(filename, 'r') as f:
            content = f.readlines()
            return content
    raise NewsNotFoundException(params[0])

def get_first_and_last(content, params):
    first = 1
    last = len(content)
    if len(params) == 2:
        first = int(params[1])
    if len(params) == 3:
        first = int(params[1])
        last = int(params[2])
    return first, last

def parse_date(datestring):
    """Parses a string of format yyyy-mm-dd into yyyy, mm-dd"""
    year, month, date = datestring.split('-')
    return year, month, date

def flat_list(content, params):
    first, last = get_first_and_last(content, params)
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
            content = '='.join(parts)  # content may/will contain ='s, reconstruct
            content = content.replace('\\n', '\n')
            items.append({'key': key.strip(), 'content': content.strip()})
            counter += 1
        elif item.strip():
            # Only count non-empty lines
            counter += 1
    return items

def items_per_year(content, params):
    first, last = get_first_and_last(content, params)
    current_year = None
    items = {}
    counter = 1
    for item in content:
        if item.strip() and first <= counter <= last:
            parts = item.split('=')
            key = parts[0]
            if key[0] == '#':
                # Skip this entry
                continue
            year, month, date = parse_date(key)
            del parts[0]
            if year != current_year:
                current_year = year
                items[year] = []
            content = '='.join(parts)  # content may/will contain ='s, reconstruct
            content = content.replace('\\n', '\n')
            items[year].append({'month': month, 'date': date, 'content': content.strip()})
            counter += 1
        elif item.strip():
            # Only count non-empty lines
            counter += 1
    return items

def render(site_path, structure, environment, params):
    """Look up the news file from site import config in site_path

    Format of params: <key>:<offset>:<length>

    :param site_path: path to the website's config and content
    :type site_path: str
    :param environment:
    """
    content = open_file(site_path, params)
    items = None
    template = environment.get_template('timeline.html')
    if 'timeline' in structure and not structure['timeline']:
        items = flat_list(content, params)
        template = environment.get_template('news.html')
        data = {'items': items, 'environment': environment}
    else:
        items = items_per_year(content, params)
    data = {'items': items, 'environment': environment}
    return template.render(data)
