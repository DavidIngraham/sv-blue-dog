"""Reproduce seasonal station counts and persistent-window diagnostics from NOAA.

python -m tools.boat_analysis.environment.climatology [--fetch]
Raw observations are frozen with hashes. No observation is a mission-success sample.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import gzip
import hashlib
import json
import urllib.request

import numpy as np

from tools.boat_analysis.model.runtime import ROOT, analysis_values
from tools.boat_analysis.evidence.records import source_hashes

DIRECTORY = ROOT / 'evidence/weather/2015-2024'
STATIONS = {'KDLS': '726988-24219', 'KTTD': '726985-24242'}
BASE = 'https://www.ncei.noaa.gov/pub/data/noaa/isd-lite'


def policy():
    return analysis_values('BlueDogWeather::Inputs')


def classify(direction, speed, p):
    """ISD-Lite direction is meteorological FROM; speed is tenths of m/s."""
    if speed < 0:
        return 'unknown'
    if speed / 10 < p['lightWindThreshold']:
        return 'light'
    if not 0 <= direction <= 360:
        return 'unknown'
    for name in ('east', 'west'):
        low, high = p[name + 'Sector']
        if low <= direction <= high:
            return name
    return 'other'


def observations(path, p):
    result = {}
    for line in gzip.decompress(path.read_bytes()).decode('ascii').splitlines():
        fields = list(map(int, line.split()))
        if len(fields) != 12:
            raise ValueError(f'Malformed ISD-Lite record in {path}')
        year, month, day, hour = fields[:4]
        date = datetime(year, month, day, hour)
        if date in result:
            raise ValueError(f'Duplicate hourly record: {date}')
        result[date] = classify(fields[7], fields[8], p)
    return result


def aggregate(records, p):
    start, stop = datetime(p['firstYear'], 1, 1), datetime(p['lastYear'] + 1, 1, 1)
    hours = [start + timedelta(hours=i) for i in range(int((stop-start).total_seconds()/3600))]
    values = np.array([records.get(t, 'unknown') for t in hours])
    season = lambda month: 'warm' if month in p['warmMonths'] else 'winter' if month in p['winterMonths'] else 'transition'
    selected = {name: [] for name in ('warm', 'winter', 'transition', 'annual')}
    width, preceding = p['windowHours'], p['precedingWestHours']
    prefixes = {key: np.r_[0, np.cumsum(values == key)] for key in ('west', 'east', 'unknown')}
    for i in range(preceding, len(hours)-width+1):
        # Only information BEFORE launch selects the window; no future filtering
        # by direction. Missing future observations make its outcome unknown.
        if prefixes['west'][i]-prefixes['west'][i-preceding] != preceding:
            continue
        complete = prefixes['unknown'][i+width]-prefixes['unknown'][i] == 0
        east = bool(prefixes['east'][i+width]-prefixes['east'][i]) if complete else None
        selected['annual'].append(east)
        selected[season(hours[i].month)].append(east)
    result = []
    for name in ('warm', 'winter', 'transition', 'annual'):
        mask = np.array([name == 'annual' or season(t.month) == name for t in hours])
        observed = sum(t in records for t, include in zip(hours, mask) if include)
        count = {key: int(np.count_nonzero((values == key) & mask)) for key in ('west', 'east', 'light', 'other', 'unknown')}
        windows = selected[name]
        result.append(dict(season=name, expectedHours=int(mask.sum()), observedHours=observed,
                           **{key+'Hours': value for key, value in count.items()},
                           selectedWindows=sum(v is not None for v in windows),
                           windowsWithEast=sum(v is True for v in windows),
                           incompleteWindows=sum(v is None for v in windows)))
    return result


def fetch_file(item):
    url, path = item
    if not path.exists():
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
        gzip.decompress(data)  # Reject HTML/error responses before preserving.
        path.write_bytes(data)
    return {'url': url, 'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def run(fetch=False):
    p = policy()
    DIRECTORY.mkdir(parents=True, exist_ok=True)
    items = [(f'{BASE}/{year}/{station}-{year}.gz', DIRECTORY/f'{station}-{year}.gz')
             for station in STATIONS.values() for year in range(p['firstYear'], p['lastYear']+1)]
    manifest_path = DIRECTORY/'manifest.json'
    if fetch:
        with ThreadPoolExecutor(max_workers=4) as pool:
            sources = list(pool.map(fetch_file, items))
        proposed = {'sources': sources}
        if manifest_path.exists() and json.loads(manifest_path.read_text()) != proposed:
            raise ValueError('Refusing to replace frozen weather evidence; use a new archive for revised sources')
        manifest_path.write_text(json.dumps(proposed, indent=2)+'\n', encoding='utf-8')
    manifest = json.loads(manifest_path.read_text())
    if {v['file'] for v in manifest['sources']} != {path.name for _, path in items}:
        raise ValueError('Archive coverage differs from model policy')
    for source in manifest['sources']:
        if hashlib.sha256((DIRECTORY/source['file']).read_bytes()).hexdigest() != source['sha256']:
            raise ValueError('Observation archive hash mismatch: '+source['file'])
    rows = []
    for station, identifier in STATIONS.items():
        records = {}
        for year in range(p['firstYear'], p['lastYear']+1):
            records.update(observations(DIRECTORY/f'{identifier}-{year}.gz', p))
        rows.extend(dict(station=station, **row) for row in aggregate(records, p))
    payload = {'policy': p, 'stations': STATIONS, 'rows': rows,
               'scope': 'UTC hourly station bins and overlapping 72-hour hindcast windows; not route or forecast-conditioned mission probabilities.'}
    output = ROOT/'build/analysis/gorge-weather.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    text = ['// Generated by tools.boat_analysis.environment.climatology from frozen NOAA observations.',
            'package BlueDogWindObservations {', '    private import ScalarValues::*;']
    for row in rows:
        text.append(f"    part {row['station']}_{row['season']} : BlueDogWeather::StationSeason {{")
        for key, value in row.items():
            text.append(f'        attribute :>> {key} = {json.dumps(value)};')
        text.append('    }')
    text.append('}')
    (ROOT/'models/evidence/gorge-wind.sysml').write_text('\n'.join(text)+'\n', encoding='utf-8')
    payload['sourceHashes'] = source_hashes(['tools/boat_analysis/environment/climatology.py', 'evidence/weather/2015-2024/manifest.json'])
    output.write_text(json.dumps(payload, indent=2)+'\n', encoding='utf-8')
    plot(rows)
    for row in rows:
        n = row['expectedHours']; axis = row['eastHours']+row['westHours']
        print(row['station'], row['season'], 'west/east/all-hours %', round(100*row['westHours']/n,1), round(100*row['eastHours']/n,1),
              'east/axis %', round(100*row['eastHours']/axis,1) if axis else None, 'east-encounter %', round(100*row['windowsWithEast']/row['selectedWindows'],1) if row['selectedWindows'] else None)


def plot(rows):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['svg.hashsalt'] = 'blue-dog-weather'
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), layout='constrained')
    for ax, station in zip(axes, STATIONS):
        subset = [r for r in rows if r['station'] == station]
        bottom = np.zeros(len(subset))
        for key, label, color in [('west','From west','#276484'),('east','From east','#bd643a'),('light','Light (<2 m/s)','#9db68e'),('other','Other direction','#acb9c3'),('unknown','Unknown / absent','#e4e6e8')]:
            values = np.array([100*r[key+'Hours']/r['expectedHours'] for r in subset])
            ax.bar([r['season'] for r in subset], values, bottom=bottom, label=label, color=color)
            bottom += values
        ax.set(title=station, ylim=(0,100), ylabel='Share of all calendar hours (%)')
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='outside lower center', ncol=3, frameon=False)
    fig.suptitle('Gorge station winds, NOAA ISD-Lite 2015–2024 (UTC)\nWarm: May–Sep · Winter: Nov–Mar · Transition: Apr/Oct')
    path = ROOT/'docs/figures/gorge-wind-seasons.svg'
    fig.savefig(path, metadata={'Date': None})
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    plt.close(fig)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true')
    run(parser.parse_args().fetch)
