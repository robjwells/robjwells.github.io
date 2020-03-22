#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import numpy as np

fields = ['Member', 'Registered', 'Affiliated', 'Total']

results_2015 = [121751 / 245520,
                88449 / 105598,
                41217 / 71546,
                251417 / 422664,
               ]
results_2016 = [168216 / (168216 + 116960),
                84918 / (84918 + 36599),
                60075 / (60075 + 39670),
                313209 / (313209 + 193229),
               ]

# data = zip(fields, results_2015, results_2016)

fig, ax = plt.subplots(figsize=(8,6))

bar_locs = np.arange(0, 8, 2)

ax.bar(bar_locs + 0.25, results_2015, label='2015',
       color='#1369BF', width=0.7, linewidth=0)
ax.bar(bar_locs + 1.05, results_2016, label='2016',
       color='#BD3338', width=0.7, linewidth=0)

ax.grid(b=False, axis='x')
ax.tick_params(width=0)
for side in ['top', 'right']:
    ax.spines[side].set_visible(False)

ax.set_ylim((0, 1))
plt.yticks(np.arange(0.1, 1.1, 0.1), np.arange(10, 110, 10))
plt.xticks(np.arange(1, 8, 2), fields)

ax.set_title('Jeremy Corbyn leadership result by section', y=1.025)
ax.set_ylabel('Percentage won')
ax.set_xlabel('Voter category', labelpad=10)

ax.legend(loc=(0.8, 0.85))

plt.savefig(
    ('/Users/robjwells/Dropbox/primaryunit/images/'
    '2016-09-25-labour_leadership.svg'),
    transparent=True, bbox_inches='tight')
