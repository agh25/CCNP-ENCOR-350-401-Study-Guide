import requests

url = 'https://192.168.1.1/restconf/data/Cisco-IOS-XE-native:native'
headers = {'Accept': 'application/yang-data+json'}
response = requests.get(url, auth=('admin', 'cisco'), headers=headers, verify=False)
print(response.json())
