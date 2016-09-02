#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import numpy as np

images_path = '/Users/robjwells/Dropbox/primaryunit/images/'

lab = np.array([11.56, 13.52, 10.72, 9.55, 8.61, 9.35])
con = np.array([14.09, 9.6, 8.34, 8.78, 10.7, 11.3])
other = np.array([7.96, 8.17, 7.3, 8.81, 10.38, 10.05])
turnout = np.array([0.777, 0.715, 0.594, 0.614, 0.651, 0.662])

years = [1992, 1997, 2001, 2005, 2010, 2015]

bar_locs = np.arange(6) * 3

ax = plt.subplot(111)
ax.grid(b=False, axis='x')
ax.tick_params(width=0)
plt.xticks(bar_locs, years[1:])
for side in ['top', 'right', 'bottom', 'left']:
    ax.spines[side].set_visible(False)


blue = '#1369BF'
red = '#BD3338'
l_grey = '#D7DBDF'
d_grey = '#AFB7BF'

lab_change = lab[1:] - lab[:-1]
non_lab_change = (con[1:] - con[:-1]) + (other[1:] - other[:-1])
total_change = lab_change + non_lab_change

ax.bar(bar_locs[:-1] - 1, lab_change,
       color=red, width=0.7, edgecolor='none',
       label='Labour')
ax.bar(bar_locs[:-1] - 0.3, non_lab_change,
       color=l_grey, width=0.7, edgecolor='none',
       label='Non-Labour')
ax.bar(bar_locs[:-1] + 0.4, total_change,
       color=d_grey, width=0.7, edgecolor='none',
       label='All votes')

ax.set_ylim(-6, 6)
ax.set_xlim(-2, 14)

ax.set_title('Change in popular vote on previous election 1997–2015')
title_x, title_y = ax.title.get_position()
ax.title.set_position((title_x, title_y + 0.025))
ax.set_ylabel('Votes (millions)')
plt.legend(loc='best')

plt.savefig(images_path + 'vote_change_1992-2015.svg',
            format='svg', transparent=True, bbox_inches='tight')

plt.cla()  # Clear axis
ax.grid(b=False, axis='x')
plt.xticks(bar_locs, years)

ax.bar(bar_locs - 0.9, lab, color=red, width=1 , edgecolor='none')
ax.bar(bar_locs + 0.1, con, color=blue, width=1, edgecolor='none')

ax.set_ylim(0, 15)
ax.set_xlim(-2, 17)

ax.set_title('Labour and Conservative vote totals 1992–2015')
ax.set_ylabel('Votes (millions)')

for side in ['top', 'right', 'bottom', 'left']:
    ax.spines[side].set_visible(False)

plt.savefig(images_path + 'lab_con_1992-2015.svg',
            format='svg', transparent=True, bbox_inches='tight')

plt.cla()  # Clear axis
ax.grid(b=False, axis='x')
plt.xticks(bar_locs, years)
ax.set_ylim(0, 51)
ax.set_xlim(-2, 17)

total_votes = lab + con + other
total_electorate = total_votes / turnout

ax.bar(bar_locs - 0.75, total_electorate, color=l_grey, width=1.5, edgecolor='none')
ax.bar(bar_locs - 0.75, total_votes, color=d_grey, width=1.5, edgecolor='none')
ax.bar(bar_locs - 0.75, lab, color=red, width=1.5, edgecolor='none')

ax.set_title('UK electorate, turnout and Labour votes 1992–2015')
ax.set_ylabel('Voters (millions)')

plt.savefig(images_path + 'lab_electorate_1992-2015.svg',
            format='svg', transparent=True, bbox_inches='tight')
