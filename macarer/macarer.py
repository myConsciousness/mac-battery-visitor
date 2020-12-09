from os import getenv
import re
import subprocess
import requests


class Macarer:

    __LINE_NOTIFY_API = 'https://notify-api.line.me/api/notify'
    __LINE_NOTIFY_TOKEN = str(getenv('LINE_NOTIFY_TOKEN_FOR_MACARER'))

    __IOREG_CAPACITY_COMMAND = '/usr/sbin/ioreg -l | /usr/bin/grep Capacity'
    __IOREG_CHARGE_COMMAND = '/usr/sbin/ioreg -l | /usr/bin/grep ExternalChargeCapable'

    def __init__(self, battery_upper_limit, battery_lower_limit):
        self.__BATTERY_UPPER_LIMIT = battery_upper_limit
        self.__BATTERY_LOWER_LIMIT = battery_lower_limit

    def examine_battery(self):

        max_capacity, current_capacity = self.__get_battery_capacities()

        if (int(max_capacity) > 0 and int(current_capacity) > 0):

            current_rate = float(current_capacity) / float(max_capacity)
            current_rate = 0
            if self.__is_charging_battery():
                if current_rate >= self.__BATTERY_UPPER_LIMIT:
                    self.__send_notification('test')
            else:
                if current_rate <= self.__BATTERY_LOWER_LIMIT:
                    self.__send_notification('test')

    def __get_battery_capacities(self):

        capacities = subprocess.check_output(self.__IOREG_CAPACITY_COMMAND, shell=True).decode(
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

    def __is_charging_battery(self):
        return True if subprocess.check_output(self.__IOREG_CHARGE_COMMAND, shell=True).decode(
            'utf-8').strip().split('=')[1].strip() == 'Yes' else False

    def __send_notification(self, message):
        requests.post(self.__LINE_NOTIFY_API, headers={
            'Authorization': 'Bearer ' + self.__LINE_NOTIFY_TOKEN}, params={'message': message})


if __name__ == '__main__':
    Macarer(0.79, 0.31).examine_battery()
