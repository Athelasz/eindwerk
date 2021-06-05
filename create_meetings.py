from convert_excel import main
import requests
import json
from environment import int_automation as env

""" Main without parameters will generate a dictionary based on
the defaults timezone:Europe/Brussels and file:list_webex.xlsx.
If another file or timezone is required you can enter one or
both underneath. """
data_dict = main()

access_token = env['token']
url = "https://webexapis.com/v1/meetings"
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

""" For every entry in the data dict the child dict is converted to
JSON and sent via a POST request to the WEBEX REST API. This creates
the meeting and checks if status_code==200. If not an error is printed"""
for m in data_dict.items():
    payload= json.dumps(m[1])
    res = requests.post(url, headers=headers, json=payload)
    if not res.status_code == 200:
        print(res.status_code,res.reason)