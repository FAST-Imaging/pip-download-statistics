import json
import pandas as pd
import requests
import os

# Get data for all the years
data = {}
for filename in os.listdir('data/'):
    if '_' not in filename and '.json' in filename:
        with open(f'data/{filename}', 'r') as file:
            data.update(json.load(file))

# Per month
df = pd.DataFrame({'date': pd.to_datetime(list(data.keys())),
                   'downloads': list(data.values())
                   })

df = df.set_index('date')
total = df.agg({'downloads': 'sum'})[0]
end_date = df.index.max()
start_date = end_date - pd.DateOffset(months=1)
df_last_month = df[df.index >= start_date]
total_last_month = df_last_month.agg({'downloads': 'sum'})[0]


def create_badge(name:str, url_string:str):
    url = f'https://img.shields.io/badge/{url_string}'

    response = requests.get(url)

    filename = f'badges/{name}.svg'
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Image downloaded successfully to {filename}")
    else:
        print('Failed')


create_badge('last_month', f'Pip_Downloads-{total_last_month}_last_month-green?logo=python')
create_badge('all_time', f'Pip_Downloads-{round(total/1000, 1)}k-green?logo=python')
