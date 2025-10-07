import json
from datetime import datetime
import json
import pandas as pd
import requests

# Get downloads over last month
year = str(datetime.now().year)

with open(f'data/{year}.json', 'r') as file:
    data = json.load(file)

# Per month
df = pd.DataFrame({'date': pd.to_datetime(list(data.keys())),
                   'downloads': list(data.values())
                   })

df = df.set_index('date')
end_date = df.index.max()
start_date = end_date - pd.DateOffset(months=1)
df_last_month = df[df.index >= start_date]
total = df_last_month.agg({'downloads': 'sum'})[0]
print(total)


url = f'https://img.shields.io/badge/pip_downloads-{total}_last_month-green?logo=python'

response = requests.get(url)

filename = 'badges/last_month.svg'
if response.status_code == 200:
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    print(f"Image downloaded successfully to {filename}")
else:
    print('Failed')