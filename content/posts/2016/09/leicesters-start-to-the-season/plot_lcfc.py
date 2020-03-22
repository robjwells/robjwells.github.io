#!/usr/local/bin/python3

from collections import defaultdict
from datetime import date

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

image_dir = '/Users/robjwells/Dropbox/primaryunit/images/'

season_files = [('2014-15', 'epl-14.txt'),
                ('2015-16', 'epl-15.txt'),
                ('2016-17', 'epl-16.txt')]

seasons = dict()


def parse_results(result_lines):
    team_records = defaultdict(list)

    for line in lines:
        if line.startswith('Matchday'):
            matchday = int(line.split()[-1])
            continue
        if line.startswith('['):
            continue
        try:
            home, score_string, away = [x.strip() for x in line.split('  ')
                                        if x.strip()]
        except:
            print(line)
        home_score, away_score = [int(d) for d in score_string.split('-')]
        if home_score == away_score:        # Draw
            home_pts, away_pts = 1, 1
        elif home_score > away_score:       # Home win
            home_pts, away_pts = 3, 0
        else:                               # Away win
            home_pts, away_pts = 0, 3
        team_records[home].append(home_pts)
        team_records[away].append(away_pts)

    return team_records


for season, results_file in season_files:
    with open(results_file) as f:
        lines = [l.strip() for l in f.readlines()
                 if l.strip()
                 if not l.startswith('#')]
        seasons[season] = parse_results(lines)


def plot_season_so_far(seasons):
    games_so_far = min([len(s['Leicester City']) for s in seasons.values()])

    fig, ax = plt.subplots(figsize=(10,5))

    for season in sorted(seasons):
        points = seasons[season]['Leicester City']
        plt.plot(np.arange(len(points)), np.cumsum(points), label=season,
                 marker='o', linewidth=2)

    plt.xlim(0, games_so_far - 1)
    plt.ylim(0, (games_so_far - 1) * 3)
    plt.xticks(np.arange(games_so_far), np.arange(1, games_so_far + 1))
    plt.yticks(np.arange(0, games_so_far * 3, 3))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    plt.title(
        'Leicester City’s first {0} games, {1} to {2} seasons'.format(
            games_so_far, min(seasons), max(seasons))
        , y=1.025)
    plt.xlabel('Games played')
    plt.ylabel('Points total')
    plt.legend(loc='best')

    plt.savefig(image_dir +
        '{0}_lcfc-first_{1}_games.svg'.format(max(seasons), games_so_far),
        transparent=True, bbox_inches='tight')
    plt.close()


def plot_all(seasons):
    fig, ax = plt.subplots(figsize=(10,7))

    plt.axhline(y=40, color='#607080', linewidth=1)
    plt.plot(np.arange(38), np.arange(1, 39) * 40/38, label='Safety',
             color='#607080', linewidth=2, linestyle='--')

    for season in sorted(seasons):
        points = seasons[season]['Leicester City']
        plt.plot(np.arange(len(points)), np.cumsum(points), label=season,
                 linewidth=2)

    plt.xlim(0, 37)
    plt.ylim(0, 85)

    plt.xticks(np.arange(0, 38, 5), np.arange(1, 39, 5))

    plt.title(
        'Leicester City points over time, {0} to {1} seasons'.format(
            min(seasons), max(seasons)),
        y=1.025)
    plt.xlabel('Games played')
    plt.ylabel('Points total')
    plt.legend(loc='best')

    plt.savefig(image_dir +
        '{0:%Y-%m-%d}_lcfc-points_over_time.svg'.format(date.today()),
        transparent=True, bbox_inches='tight')
    plt.close()

def plot_adrift(seasons):
    fig, ax = plt.subplots(figsize=(10, 5))
    safety_trend = np.arange(1, 39) * 40/38

    plt.axhline(y=0, color='#607080', linewidth=1)

    for season in sorted(seasons):
        points = seasons[season]['Leicester City']
        plt.plot(np.arange(len(points)),
                 np.cumsum(points) - safety_trend[:len(points)],
                 label=season, linewidth=2)

    plt.xlim(0, 37)

    plt.xticks(np.arange(0, 38, 5), np.arange(1, 39, 5))

    plt.title(
        'Leicester City points distant from safety trend, {0} to {1} seasons'.format(
            min(seasons), max(seasons)),
        y=1.025)
    plt.xlabel('Games played')
    plt.ylabel('Points difference')
    plt.legend(loc='best')

    plt.savefig(image_dir +
        '{0:%Y-%m-%d}_lcfc-points_adrift.svg'.format(date.today()),
        transparent=True, bbox_inches='tight')
    plt.close()


def plot_relegated(seasons):
    teams = ['Aston Villa', 'Norwich City', 'Newcastle United', 'Sunderland AFC']
    colours = ['#58092B', '#00A94F', '#000000', '#DE2027']

    fig, ax = plt.subplots(figsize=(10, 5))
    safety_trend = np.arange(1, 39) * 40/38
    plt.axhline(y=0, color='#607080', linewidth=1)

    for team, colour in zip(teams, colours):
        points = seasons['2015-16'][team]
        line_style = '--' if team == 'Sunderland AFC' else '-'
        plt.plot(np.arange(len(points)),
                 np.cumsum(points) - safety_trend[:len(points)],
                 label=team, linewidth=2, color=colour, linestyle=line_style)

    plt.xlim(0, 37)

    plt.xticks(np.arange(0, 38, 5), np.arange(1, 39, 5))

    plt.title(
        'Bottom four teams’ distance from safety trend, 2015-16 season',
        y=1.025)
    plt.xlabel('Games played')
    plt.ylabel('Points difference')
    plt.legend(loc='best')

    plt.savefig(image_dir +
        '{0:%Y-%m-%d}_lcfc-bottom_4_points_adrift.svg'.format(date.today()),
        transparent=True, bbox_inches='tight')
    plt.close()



plot_season_so_far(seasons)
plot_all(seasons)
plot_adrift(seasons)
plot_relegated(seasons)
