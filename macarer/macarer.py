from os import getenv
import re
import sys
import subprocess
import requests

BATTERY_UPPER_LIMIT = 0.79
BATTERY_LOWER_LIMIT = 0.31

IOREG_CAPACITY_COMMAND = '/usr/sbin/ioreg -l | /usr/bin/grep Capacity'
IOREG_CHARGE_COMMAND = '/usr/sbin/ioreg -l | /usr/bin/grep ExternalChargeCapable'

LINE_NOTIFY_API = 'https://notify-api.line.me/api/notify'
LINE_NOTIFY_TOKEN = str(getenv('LINE_NOTIFY_TOKEN_FOR_MACARER'))


def examine_battery():

    max_capacity, current_capacity = get_battery_capacities()

    if (int(max_capacity) > 0 and int(current_capacity) > 0):

        rate = float(current_capacity) / float(max_capacity)

        if is_charging_battery():
            if rate >= BATTERY_UPPER_LIMIT:
                send_notification('')
        else:
            if rate <= BATTERY_LOWER_LIMIT:
                send_notification('')


def get_battery_capacities():

    capacities = subprocess.check_output(IOREG_CAPACITY_COMMAND, shell=True).decode(
        'utf-8').strip().split('\n')

    max_capacity = 0
    current_capacity = 0

    for st in capacities:
        ar = st.split('=')
        key = re.sub('^(.*?")', '', ar[0]).replace('" ', '')

        if (key == 'MaxCapacity'):
            max_capacity = ar[1].strip()
        elif key == 'CurrentCapacity':
            current_capacity = ar[1].strip()

    return max_capacity, current_capacity


def is_charging_battery():
    return True if subprocess.check_output(IOREG_CHARGE_COMMAND, shell=True).decode(
        'utf-8').strip().split('=')[1].strip() == 'Yes' else False


def send_notification(message):
    requests.post(LINE_NOTIFY_API, headers={
        'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN}, params={'message': message})


if __name__ == '__main__':
    examine_battery()
