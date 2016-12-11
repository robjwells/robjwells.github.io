#!/usr/local/bin/python3

from datetime import datetime, timedelta
import json
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt, dates as mdates

json_files = {
    'DB': '20161210-DB-Berlin-Leipzig.json',
    'East Mids': '20161210-EMT-London-Leicester.json',
    'NS': '20161210-NS-Amsterdam-Eindhoven.json',
    'SNCF': '20161210-SNCF-ParisNord-Amiens.json',
    }


def parse_json_entry(line):
    """Convert a [time, cost] list read from file into native types"""
    time_str, cost = line
    time = datetime.strptime('2016-12-23 {}'.format(time_str),
                             '%Y-%m-%d %H:%M')
    return (time, cost)


train_data = {
    operator: [parse_json_entry(p)
               for p in json.loads(s=Path(fn).read_text(),
                                   parse_float=float)]
    for operator, fn in json_files.items()
    }

operator_colors = {
    'DB': '#1369BF',
    'East Mids': '#BD3338',
    'NS': '#00800A',
    'SNCF': '#7436B3'
    }
operator_markers = {
    'DB': 'o',
    'East Mids': '^',
    'NS': 's',
    'SNCF': '*'
    }

# Order operator by average price (known in advance)
operator_order = {
    'DB': 2,
    'East Mids': 1,
    'NS': 4,
    'SNCF': 3
    }

fig, ax = plt.subplots(figsize=(10,5))
for operator, data in sorted(train_data.items(),
                             key=lambda x: operator_order[x[0]]):
    times = mdates.date2num([x[0] for x in data])
    costs = np.array([x[1] for x in data])

    plt.plot(
        times, costs,
        operator_markers[operator],
        color=operator_colors[operator],
        label=operator,
        markeredgewidth=1,
        markersize=8)

hours = [datetime(2016, 12, 23, 14) + timedelta(seconds=x * 60 * 60)
         for x in range(11)]

plt.xticks(
    mdates.date2num(hours),
    [h.strftime('%H:%M') for h in hours]
    )
plt.xlim((
    mdates.date2num(datetime(2016, 12, 23, 13, 45)),
    mdates.date2num(datetime(2016, 12, 24, 0))
    ))
plt.ylim((0, 100))
plt.yticks(range(10, 101, 10))
plt.xlabel('Time')
plt.ylabel('Ticket cost (€)')
plt.title('Cost of single train tickets leaving European\ncapital cities on Friday December 23 2016',
          y=1.025)

plt.legend(loc='best', numpoints=1)
plt.savefig('test.svg', transparent=True, bbox_inches='tight')
