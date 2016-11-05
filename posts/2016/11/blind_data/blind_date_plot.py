#!/usr/local/bin/python3

from collections import Counter, defaultdict
import csv

from matplotlib import pyplot as plt
import numpy as np

image_dir = '/Users/robjwells/Dropbox/primaryunit/images/'

scores = []
meet_counters = defaultdict(Counter)

with open('blind_date_reviewed.csv', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file,
                            fieldnames=['_s', '_m', 'score', 'meet'])
    next(reader)    # Skip headers
    for row in reader:
        scores.append(float(row['score']))
        meet_counters[float(row['score'])].update([
            True if row['meet'] is 'Y' else False
            ])

poss_scores = np.arange(0, 10.5, 0.5)

ratios = {score: c[True] / (c[True] + c[False])
          for score, c in sorted(meet_counters.items())}
all_nums = {float(x): 0.0 for x in poss_scores}
all_nums.update(ratios)
ratios_array = np.array([r for i, r in sorted(all_nums.items())])

all_nums = {float(x): 0.0 for x in poss_scores}
all_nums.update(Counter(scores))
scores_array = np.array([t for i, t in sorted(all_nums.items())])


fig, ax = plt.subplots(figsize=(10, 7))
ax.bar(poss_scores, scores_array,
       linewidth=1, width=0.5, color='#AFB7BF',
       label='All dates')
ax.bar(poss_scores, scores_array * ratios_array,
       linewidth=0.5, width=0.5, color='#BD3338',
       label='Would meet date again')

ax.set_xlim((0, 10.5))
ax.set_xticks(np.arange(0.25, 10.5, 1))
ax.set_xticklabels(map(int, poss_scores[::2]))
ax.tick_params(width=0)
ax.set_xlabel('Score, in half-point intervals')

ax.set_yticks(np.arange(25, 201, 25))
ax.set_ylabel('Score frequency')

ax.grid(b=False, axis='x')
ax.set_title('Guardian Blind Date score distribution, Jan 2009–Oct 2016',
             y=1.025)

ax.legend(loc='best')

plt.savefig(image_dir + '2016-11-05-score_distribution.svg',
            transparent=True, bbox_inches='tight')
ax.cla()


fig, ax = plt.subplots(figsize=(10, 7))
ax.bar(poss_scores, ratios_array * 100,
       linewidth=0.5, width=0.5, color='#1369BF')

ax.set_xlim((6, 10.5))
ax.set_xticks(np.arange(6.25, 10.5, 0.5))
ax.set_xticklabels([int(x) if x.is_integer() else x
                    for x in np.arange(6, 10.5, 0.5)])
ax.tick_params(width=0)
ax.set_xlabel('Score')

ax.set_yticks(np.arange(25, 101, 25))
ax.set_ylabel('% Yes to “Would you meet again?”')

ax.grid(b=False, axis='x')
ax.set_title('Desire for second date by score', y=1.025)

plt.savefig(image_dir + '2016-11-05-interest_rate.svg',
            transparent=True, bbox_inches='tight')
