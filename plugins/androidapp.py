"""
paragoo plugin for retrieving card on an Android app
"""
import os
import requests
from bs4 import BeautifulSoup


class AppNotFoundException(Exception):
    pass


def render(site_path, params):
    """
    Look up the Android app details from its Play Store listing
    Format of params: <app_key>
    app_key looks like com.linkbubble.license.playstore
    """
    app_key = params[0]
    url_full = 'https://play.google.com/store/apps/details?id=' + app_key
    url = 'https://play.google.com/store/apps/details'
    url_params = {'id': app_key }
    result = requests.get(url, params=url_params)
    if result.status_code != requests.codes.ok:
        raise AppNotFoundException(params[0])
    else:
        soup = BeautifulSoup(result.text, 'html.parser')
        # TODO: render a card(?) with the site's androidapp.html template
        return '<a href="' + url_full + '">' + soup.title.text.replace(' - Android-apps op Google Play', '') + '</a>'
