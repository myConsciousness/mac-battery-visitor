from subprocess import Popen, PIPE
import sys
import requests

cmd = '/usr/sbin/ioreg -l | /usr/bin/grep Capacity'

output = Popen(cmd.split(), stdout=PIPE).communicate()[0]
output_str = str(output, encoding='utf-8')

battery_info = dict(
    [(kw.strip().strip('"'), vw.strip())
     for kw, vw
     in [line.split("=", 1)
         for line
         in output_str.split('\n') if line.find('=') > 0
         ]
     ]
)

# mAh
current_capa = int(battery_info["CurrentCapacity"])
# mAh
max_capa = int(battery_info["MaxCapacity"])

charge_ratio = int((current_capa/max_capa) * 100)

url = 'https://notify-api.line.me/api/notify'
token = 'xxxxxxx'
headers = {'Authorization': 'Bearer ' + token}

if charge_ratio >= 90:
    message = ''
    payload = {"message": message}
    r = requests.post(url, headers=headers, params=payload)
elif charge_ratio <= 20:
    message = ''
    payload = {"message": message}
    r = requests.post(url, headers=headers, params=payload)
