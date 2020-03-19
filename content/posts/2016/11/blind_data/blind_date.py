#!/usr/local/bin/python3

import csv
import json
import re

from bs4 import BeautifulSoup

score_text = re.compile(r'Marks out of 10?')
meet_text = re.compile('Would you meet again?')

all_scores = []
all_meets = []

with open('blind_date.json') as json_file:
    articles = json.load(json_file)

for article in articles:
    soup = BeautifulSoup(article['fields']['body'], 'lxml')
    try:
        scores = [n.find_parent('p') for n in soup.find_all(text=score_text)]
        meets = [n.find_parent('p') for n in soup.find_all(text=meet_text)]

        if len(scores) != 2 or len(meets) != 2:
            print(soup, end='\n\n\n')
        else:
            all_scores.extend(
                [s.text.split(score_text.pattern)[1].strip(' .')
                 for s in scores]
                )
            all_meets.extend(
                [s.text.split(meet_text.pattern)[1].strip(' .')
                 for s in meets]
            )
    except (AttributeError, IndexError):
        print(soup)

paired = zip(all_scores, all_meets)

with open('blind_date.csv', mode='w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow((score_text.pattern, meet_text.pattern))
    for pair in paired:
        writer.writerow(pair)
