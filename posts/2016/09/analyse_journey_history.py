#!/usr/local/bin/python3

from collections import Counter
import csv
from datetime import datetime, timedelta
import decimal
from pathlib import Path
import re

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates

headers = ['Date',
           'Start Time',
           'End Time',
           'Journey/Action',
           'Charge',
           'Credit',
           'Balance',
           'Note',
           ]


def parse_journey_row(row):
    """Convert journey history dict of strings to appropriate types"""
    row['Date'] = datetime.strptime(row['Date'], '%d-%b-%Y')

    if row['Start Time']:
        start_time = datetime.strptime(row['Start Time'], '%H:%M')
        start_date = row['Date'].replace(hour=start_time.hour,
                                         minute=start_time.minute)
        row['Start Time'] = start_date

    if row['End Time']:
        end_time = datetime.strptime(row['End Time'], '%H:%M')
        end_date = row['Date'].replace(hour=end_time.hour,
                                       minute=end_time.minute)
        if row['Start Time']:
            # Handle past-midnight journeys
            adjust = 1 if end_time < start_time else 0
            end_date = end_date + timedelta(adjust)

        row['End Time'] = end_date

    if ' to ' in row['Journey/Action']:
        row['Journey/Action'] = row['Journey/Action'].split(' to ')

    for key in ['Balance', 'Charge', 'Credit']:
        if row[key]:
            row[key] = decimal.Decimal(row[key])

    return row


def sort_by_time(entry):
    """Return journey entry's Start Time, End Time, or Date"""
    if entry['Start Time']:
        return entry['Start Time']
    elif entry['End Time']:
        return entry['End Time']
    else:
        return entry['Date']


all_entries = []

csv_dir = Path('/Users/robjwells/Documents/Oyster card/Journey history CSVs')
for csv_path in csv_dir.glob('*.csv'):
    with csv_path.open() as csv_file:
        read_rows = [parse_journey_row(row) for row in
                     csv.DictReader(csv_file, fieldnames=headers)
                     if not row['Date'] == 'Date']
        all_entries.extend(read_rows)


all_entries.sort(key=sort_by_time)

earliest_date = min([e['Date'] for e in all_entries])
latest_date = max([e['Date'] for e in all_entries])

charges = [(e['Date'], e['Charge']) for e in all_entries if e['Charge']]

top_ups = []
refunds = []
bus_journeys = []
tube_journeys = []
others = []

for entry in all_entries:
    if type(entry['Journey/Action']) == list:
        tube_journeys.append(entry)
        continue
    if 'Auto top-up' in entry['Journey/Action']:
        top_ups.append(entry)
        continue
    if 'refund' in entry['Journey/Action'].lower():
        refunds.append(entry)
        continue
    if 'Bus journey' in entry['Journey/Action']:
        bus_journeys.append(entry)
        continue
    else:
        others.append(entry)

start_stations = []
end_stations = []
journey_lengths = []
start_and_end = []

for journey in tube_journeys:
    start, end = journey['Journey/Action']
    station_regex = re.compile(r'''
        ^
        <?                                # Refund in progress bracket
        (
            \[ No \s touch-(?:in|out) \]
        |
            (?:[\w'&-]+\s*?)+              # Station name
        )
        \s?
        (?:[[(] [^)\]]+ [\])])?           # Station qualifier '[National rail]'
        (?:DLR)?                          # DLR station suffix
        >?                                # Refund in progress bracket
        $
    ''', flags=re.X)
    start = station_regex.match(start).group(1)
    end = station_regex.match(end).group(1)
    start_stations.append(start)
    end_stations.append(end)
    start_and_end.append((start, end))


    if journey['Start Time'] and journey['End Time']:
        journey_seconds = (journey['End Time'] - journey['Start Time']).seconds
        journey_lengths.append(
            (int(journey_seconds / 60), journey))

start_stations = Counter(start_stations)
end_stations = Counter(end_stations)
journey_lengths.sort(key=lambda x: x[0])
del journey_lengths[0]  # Delete artificially short journey (no touch out)

station_pairs = [frozenset(pair) for pair in start_and_end]
station_pairs = Counter(station_pairs)
start_and_end = Counter(start_and_end)


def plot_weekly_spending():
    rolling_week_end = earliest_date + timedelta(6)
    weekly_totals = []
    while rolling_week_end <= latest_date:
        interesting = [c for d, c in charges
                       if 0 <= (rolling_week_end - d).days <= 6]
        weekly_totals.append((rolling_week_end, sum(interesting)))
        rolling_week_end += timedelta(7)

    # Work out weekly averages over four-week periods
    rolling_month_end = earliest_date + timedelta(55)
    weekly_averages = []
    while rolling_month_end <= latest_date:
        interesting = [c for d, c in charges
                       if 0 <= (rolling_month_end - d).days <= 55]
        weekly_averages.append((rolling_month_end, sum(interesting) / 8))
        rolling_month_end += timedelta(7)

    fig, ax = plt.subplots(figsize=(12,5))

    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b '%y"))
    plt.xlim((datetime(2014,9,1), datetime(2016,9,1)))

    dates = [d for d, _ in weekly_totals]

    plt.axhline(y=10, xmin=0, xmax=1, color='#607080', linewidth=0.75)
    plt.axhline(y=15, xmin=0, xmax=1, color='#607080', linewidth=0.75)

    totals = [c for _, c in weekly_totals]
    ax.plot(dates, totals, 'o', markersize=3, markeredgewidth=0,
            label='Totals')

    w_dates = [d for d, _ in weekly_averages]
    w_totals = [c for _, c in weekly_averages]
    ax.plot(w_dates, w_totals, linewidth=2, label='Averages')

    plt.title('Weekly transport spending and six-week moving average', y=1.025)
    plt.ylabel('Cost (£)')

    for side in ['top', 'right', 'bottom', 'left']:
        ax.spines[side].set_visible(False)
    ax.tick_params(top=False, right=False, bottom=False, left=False)

    plt.savefig('weekly_spending.svg', transparent=True, bbox_inches='tight')
    plt.gcf().clear()


def plot_journey_length_histogram():
    fig, ax = plt.subplots(figsize=(12,5))
    plt.hist([x[0] for x in journey_lengths[:-1]], bins=16, range=(0,80),
             linewidth=0.5)

    for side in ['top', 'right']:
        ax.spines[side].set_visible(False)
    ax.tick_params(top=False, right=False)

    plt.xlabel('Length of journey (minutes, in 5-minute groups)')
    plt.ylabel('Number of journeys')
    plt.title('Journey time', y=1.025)

    plt.savefig('journey_lengths.svg', transparent=True, bbox_inches='tight')
    plt.gcf().clear()


def plot_common_stations():
    top_pairs = list(reversed(station_pairs.most_common(10)))
    pair_strings = [' - '.join(sorted(x[0])) for x in top_pairs]
    pair_strings[-2] = pair_strings[-2].replace('International', 'Int’l')
    pair_strings = [ps.replace('Woolwich Arsenal', 'Woolwich')
                    for ps in pair_strings]
    pair_strings = [
        ps.replace(' - ', '\n←→ ')
        if len(ps.split(' - ')[0]) > len(ps.split(' - ')[1])
        else ps.replace(' - ', ' ←→\n')
        for ps in pair_strings]

    bar_locs = np.arange(10) + 0.1

    fig, ax = plt.subplots(figsize=(9,6))
    ax.barh(bar_locs, [x[1] for x in top_pairs], color='#1369BF', linewidth=0)

    plt.yticks(bar_locs + 0.375, pair_strings)
    ax.grid(b=False, axis='y')
    for side in ['top', 'right', 'left', 'bottom']:
        ax.spines[side].set_visible(False)
    ax.tick_params(top=False, right=False, bottom=False, left=False)

    plt.title('Most common journey endpoints', y=1.025, x=0.4)
    plt.xlabel('Number of journeys')
    plt.savefig('station_pairs.svg', transparent=True, bbox_inches='tight')
    plt.gcf().clear()


def plot_journey_hours():
    fig, ax = plt.subplots(figsize=(12,5))
    has_start = [x['Start Time'].hour for x in tube_journeys if x['Start Time']]
    has_start = [x + 25 if x == 0 else x for x in has_start]
    plt.hist(has_start, range=(5,25), bins=20, linewidth=0.5)
    plt.xlim(5,25)

    for side in ['top', 'right']:
        ax.spines[side].set_visible(False)
    ax.tick_params(top=False, right=False, bottom=False)
    ax.grid(b=False, axis='x')


    hour_labels = list(range(5, 24)) + [0]
    plt.xticks(np.arange(5, 25) + 0.5, hour_labels)

    plt.xlabel('Hour of day')
    plt.ylabel('Number of journeys')
    plt.title('Journeys by hour started', y=1.025)
    plt.savefig('journeys_by_hour.svg', transparent=True, bbox_inches='tight')


### Reporting

def write_report():
    with open('journey_report.txt', mode='w', encoding='utf-8') as report_file:
        report = []
        report.append(
            'Journey statistics: {0:%a %b %-d %Y} to {1:%a %b %-d %Y}'
            .format(earliest_date, latest_date))

        ## Journey charges
        report.append(
            'Total journey charges: £{0:,}'.format(sum([x[1] for x in charges])))

    ## Top-ups

        report.append(
            'Times topped-up: {0}, roughly every {1} days'
            .format(len(top_ups), round(700/72)))

    ## Bus journeys

        bus_routes = Counter(
            [x['Journey/Action'].split('route ')[1] for x in bus_journeys])

        report.append('\n'.join([
            'Bus journeys taken: {0}'.format(len(bus_journeys)),
            ('Bus journeys taken between midnight and 4am: {0}'
            .format(len([j for j in bus_journeys if j['Start Time'].hour < 4]))),
            'Bus journeys by route:',
            *['{0}    {1}'.format(times_taken, route) for
              route, times_taken in bus_routes.most_common()]
            ]))

    ## Tube journeys

        report.append(
            'Tube/rail journeys taken: {0}'.format(len(tube_journeys) - 2))
        # -2 for 2 boat trips made

        shortest = []
        for minutes, journey in journey_lengths[:10]:
            line = '{0:>3}    {1:%Y-%m-%d %H:%M}    {2}'.format(
                minutes, journey['Start Time'],
                ' to '.join(journey['Journey/Action']))
            shortest.append(line)

        report.append('\n'.join([
            '10 shortest journeys:',
            *shortest]))

        longest = []
        for minutes, journey in journey_lengths[-10:]:
            line = '{0:>3}    {1:%Y-%m-%d %H:%M}    {2}'.format(
                minutes, journey['Start Time'],
                ' to '.join(journey['Journey/Action']))
            longest.append(line)

        report.append('\n'.join([
            '10 longest journeys:',
            *longest]))



        total_journey_minutes = sum([x[0] for x in journey_lengths])
        total_journey_hours = total_journey_minutes // 60
        remainder_minutes = total_journey_minutes % 60

        report.append('\n'.join([
            'Time spent in the Tube network: {0} hours, {1} minutes'
            .format(total_journey_hours, remainder_minutes),

            'Mean journey length: {0} minutes'
            .format(round(total_journey_minutes / len(tube_journeys))),

            'Median journey length: {0} minutes'
            .format(journey_lengths[len(journey_lengths) // 2 - 1][0]),

            'Mode journey length: {0} minutes'
            .format(Counter([x[0] for x in journey_lengths]).most_common(1)[0][0])
            ]))


        report.append('\n'.join([
            '10 most common journeys:',

            *['{0:>3}    {1:25}    {2}'.format(times_made, pair[0], pair[1])
              for pair, times_made in start_and_end.most_common(10)]
            ]))


        report.append('\n'.join([
            '10 most common station pairs (start or end):',

            *['{0:>3}    {1:25} {2}'.format(appearances, *pair)
             for pair, appearances in station_pairs.most_common(10)]
             ]))

        report.append(
            'Total number of stations used to start or end a journey: ' +
            str(len(set(start_stations + end_stations)) - 2)  # - No touch-in/out
            )

        report.append('\n'.join([
            'Stations entered but not exited:',
            *sorted(set(start_stations) - set(end_stations))
            ]))

        report.append('\n'.join([
            'Stations exited but not entered:',
            *sorted(set(end_stations) - set(start_stations))
            ]))

        report_file.write('\n\n'.join(report))

if __name__ == '__main__':
    plot_weekly_spending()
    plot_journey_length_histogram()
    plot_common_stations()
    plot_journey_hours()
    write_report()
