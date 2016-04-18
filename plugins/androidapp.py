"""
paragoo plugin for retrieving card on an Android app
"""
import os
import requests
from bs4 import BeautifulSoup


class AppNotFoundException(Exception):
    pass


def get_app_details(app_key):
    url_full = 'https://play.google.com/store/apps/details?id=' + app_key
    url = 'https://play.google.com/store/apps/details'
    url_params = {'id': app_key }
    result = requests.get(url, params=url_params)
    if result.status_code != requests.codes.ok:
        raise AppNotFoundException(params[0])
    else:
        soup = BeautifulSoup(result.text, 'html.parser')
        #desc_blocks = soup.find('div', {'id': 'id-app-orig-desc'})
        desc_blocks = soup.findAll('div', attrs={'class':'show-more-content'})
        description = ''
        if len(desc_blocks) > 0:
            description = desc_blocks[0]
            try:
                # Get the first (language) block, likely english
                children = desc_blocks[0].findChildren()
                description = children[0]
            except KeyError:
                pass
        return {'title': soup.title.text.replace(' - Android-apps op Google Play', ''), 'url': url_full, 'description': description, 'app_id': app_key}


def render(site_path, environment, params):
    """
    Look up the Android app details from its Play Store listing
    Format of params: <app_key>:optional description
    app_key looks like com.linkbubble.license.playstore
    """
    app_key = params[0]
    details = get_app_details(app_key)
    try:
        details['notes'] = params[1]
        if len(params) > 2:
            # The description contained one or more colons, lets fix this
            details['notes'] = ':'.join(params[1:])
    except IndexError:
        pass
    # TODO: render a card(?) with the site's androidapp.html template
    #return '<a href="' + details['url'] + '">' + details['title'] + '</a>'
    template = environment.get_template('androidapp.html')
    return template.render(details)
