import pypistats
import json
import os
from datetime import datetime, timedelta

year = str(datetime.now().year)
date_format = '%Y-%m-%d'


def initialize(filename):
    since_date = f'{year}-01-01'
    # End date should be yesterday
    end_date = (datetime.now() - timedelta(days=1)).strftime(date_format)
    if os.path.exists('data/last_updated'):
        with open('data/last_updated', 'r') as file:
            since_date = file.readline().strip()
            # Add one day
            since_date = (datetime.strptime(since_date, date_format) + timedelta(days=1)).strftime(date_format)

    # Check if JSON file exists
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    return since_date, end_date, data


# =====================> Total downloads
since_date, end_date, data = initialize(f'data/{year}.json')
total = pypistats.overall('pyfast', mirrors=False, total='daily', format='json', start_date=since_date, end_date=end_date)
raw_data = json.loads(total)
print('New entries:', len(raw_data['data']))

for entry in raw_data['data']:
    data[entry['date']] = entry['downloads']

# Sort by key
sorted_data = dict(sorted(data.items()))

with open(f'data/{year}.json', 'w') as file:
    json.dump(sorted_data, file, indent=4)


# ==============> Per operating system
since_date, end_date, data = initialize(f'data/{year}_OS.json')
total = pypistats.system('pyfast', total='daily', format='json', start_date=since_date, end_date=end_date)
raw_data = json.loads(total)
print('New entries:', len(raw_data['data']))

for OS in [('Darwin', 'macOS'), ('Windows', 'Windows'), ('Linux', 'Linux'), ('null', 'Unknown')]:
    if OS[1] not in data:
        data[OS[1]] = {}
    for entry in raw_data['data']:
        if entry['category'] == OS[0]:
            data[OS[1]][entry['date']] = entry['downloads']

    # Sort by key
    data[OS[1]] = dict(sorted(data[OS[1]].items()))

with open(f'data/{year}_OS.json', 'w') as file:
    json.dump(data, file, indent=4)


# ==============> Per python version
since_date, end_date, data = initialize(f'data/{year}_python_version.json')
total = pypistats.python_minor('pyfast', total='daily', format='json', start_date=since_date, end_date=end_date)
raw_data = json.loads(total)
print('New entries:', len(raw_data['data']))

# Get highest python version
highest_minor_version = 10
for entry in raw_data['data']:
    minor_version = entry['category'].split('.')[-1]
    if minor_version != 'null':
        minor_version = int(minor_version)
        if minor_version > highest_minor_version: highest_minor_version = minor_version
for key in data.keys():
    minor_version = key.split('.')[-1]
    if minor_version != 'Unknown':
        minor_version = int(minor_version)
        if minor_version > highest_minor_version: highest_minor_version = minor_version

for version in list(range(6, highest_minor_version+1))+['null',]:
    if version == 'null':
        version_str = 'null'
    else:
        version_str = f'3.{version}'
    key = 'Unknown' if version == 'null' else version_str
    if key not in data:
        data[key] = {}
    for entry in raw_data['data']:
        if entry['category'] == version_str:
            data[key][entry['date']] = entry['downloads']

    # Sort by key
    data[key] = dict(sorted(data[key].items()))

with open(f'data/{year}_python_version.json', 'w') as file:
    json.dump(data, file, indent=4)


# =====================> Update last_updated file
with open('data/last_updated', 'w') as file:
    file.write(end_date)
