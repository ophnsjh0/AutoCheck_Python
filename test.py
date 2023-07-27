import requests

user = 'nsroot'
password = 'wkdb1100'


url = 'https://172.20.2.8/nitro/v1/config/' 
response = requests.get(url, auth=(user, password))
data = response.json()
for config_object in data['configobjects']:
  stat_url_test = 'http://172.20.2.8/nitro/v1/config/lbvserver' 
  response = requests.get(stat_url_test, auth=(user, password))
  if response.status_code == 200:
    print(config_object)