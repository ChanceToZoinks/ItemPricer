import requests

params = {'league': 'Harbinger'}
r = requests.get('http://api.poe.ninja/api/Data/GetCurrencyOverview', params=params)
rr = r.json()

print(rr)