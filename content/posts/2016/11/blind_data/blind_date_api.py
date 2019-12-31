#!/usr/local/bin/python3

import json

import keyring
import requests

api_key = keyring.get_password('guardianapi', 'robjwells')
endpoint = 'http://content.guardianapis.com/lifeandstyle/series/blind-date'

articles = []
basic_params = {'api-key': api_key, 'show-fields': 'body'}
first_page = requests.get(
    endpoint,
    params=basic_params
).json()['response']

total_pages = first_page['pages']

articles.extend(first_page['results'])

for page_no in range(2, total_pages + 1):
    resp = requests.get(
        endpoint,
        params=dict(**basic_params, page=page_no)
    ).json()
    articles.extend(resp['response']['results'])

with open('blind_date.json', mode='w') as json_file:
    json.dump(articles, json_file)
