#!/usr/local/bin/python3

from datetime import datetime
import json
from pathlib import Path

with open('tumblr-urls.json') as json_file:
    tumblr_pairs = json.load(json_file)

tumblr_pairs = [[url, datetime.strptime(date_string, '%Y-%m-%d')]
                for url, date_string in tumblr_pairs]
tumblr_pairs.sort(key=lambda pair: pair[1], reverse=True)
output_path = Path('site')

for url, date in tumblr_pairs:
    tumblr_id, slug = url.split('/')[-2:]
    post_path = output_path.joinpath('{d:%Y/%m/}{s}/'.format(d=date, s=slug))
    if post_path.exists():
        template = 'rewrite {id} /{path}/ permanent;'
        print(template.format(id=tumblr_id,
                              path=post_path.relative_to(output_path)))
