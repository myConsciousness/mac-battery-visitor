"""
Copyright 2020 Kato Shinya.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. See the License for the specific language governing permissions and limitations under
the License.
"""

from os import getenv
import re
import subprocess
import requests


class Macarer:
    """
    Macarer is a script created to optimize the battery status of a MacBook, which monitors the battery status of the MacBook.
    Macarer sends notifications to a specified Line room when it detects overcharged and undercharged conditions.

    By default, the environment variable 'LINE_NOTIFY_TOKEN_FOR_MACARER' must be set to the token associated with the Line room you are sending to.

    Example for run by default:
        Macarer().examine()

    Example for run with specific battery limits:
        Macarer(battery_upper_limit=0.80,
                battery_lower_limit=0.40).examine()

    Example for run with specific line notify token:
        Macarer(line_notify_token='0123456789abcdefghijk').examine()
    """

    # The url of the Line Notify API
    __LINE_NOTIFY_API = 'https://notify-api.line.me/api/notify'

    # The unix command for battery capacity
    __IOREG_CAPACITY_COMMAND = '/usr/sbin/ioreg -l | /usr/bin/grep Capacity'
    # The unix command for battery state
    __IOREG_CHARGE_COMMAND = '/usr/sbin/ioreg -l | /usr/bin/grep ExternalChargeCapable'

    # The template of message
    __MESSAGE_TEMPLATE = """
Detected {title} of MacBook that you own.

{caution} to optimize the battery condition of your MacBook.
Current Battery rate: {current_capacity}%
    """

    def __init__(self, battery_upper_limit=0.71, battery_lower_limit=0.31, line_notify_token=str(getenv('LINE_NOTIFY_TOKEN_FOR_MACARER'))):
        """
        The constructor.

        Args:
            battery_upper_limit (float, optional): The upper limit of the battery. Defaults to 0.71.
            battery_lower_limit (float, optional): The lower limit of the battery. Defaults to 0.31.
            line_notify_token (str, optional): The token associated with the room of Line Notify.

        Raises:
            ValueError: When the upper limit is less than 0.1, or the lower limit is less than 0.1
            ValueError: When the token is empty
        """

        if battery_upper_limit < 0.1 or battery_lower_limit < 0.1:
            raise ValueError(
                'The upper and lower limits must be greater than 0.0.')
        elif not line_notify_token:
            raise ValueError('A valid token must be specified.')

        self.__BATTERY_UPPER_LIMIT = battery_upper_limit
        self.__BATTERY_LOWER_LIMIT = battery_lower_limit
        self.__LINE_NOTIFY_TOKEN = line_notify_token

    def examine(self):
        """
        Check MacBook's battery status and remaining charge and send a notification to the Line room associated with the token. Send nitification when the battery is charging and has exceeded the upper limit, or the battery is not charging and is below the lower limit.
        """

        max_capacity, current_capacity = self.__get_battery_capacities()

        if (int(max_capacity) > 0 and int(current_capacity) > 0):

            current_rate = float(current_capacity) / float(max_capacity)

            if self.__is_charging_battery():
                if current_rate >= self.__BATTERY_UPPER_LIMIT:
                    self.__send_notification(
                        title='the undercharge',
                        current_capacity=str(current_capacity)
                    )
            else:
                if current_rate <= self.__BATTERY_LOWER_LIMIT:
                    self.__send_notification(
                        title='the overcharging',
                        current_capacity=str(current_capacity)
                    )

    def __get_battery_capacities(self):
        """
        Returns the battery capacities of the MacBook from the Unix command.

        Returns:
            str: The max capacity of the battery
            str: The current capacity of the battery
        """

        capacities = subprocess.check_output(self.__IOREG_CAPACITY_COMMAND, shell=True).decode(
            'utf-8').strip().split('\n')

        max_capacity = 0
        current_capacity = 0

        for capacity in capacities:
            entry_set = capacity.split('=')
            key = re.sub('^(.*?")', '', entry_set[0]).replace('" ', '')

            if (key == 'MaxCapacity'):
                max_capacity = entry_set[1].strip()
            elif key == 'CurrentCapacity':
                current_capacity = entry_set[1].strip()

        return max_capacity, current_capacity

    def __is_charging_battery(self) -> bool:
        """
        Tests whether the MacBook is charging or not.

        Returns:
            bool: True if the MacBook is charging, otherwise False
        """

        return True if subprocess.check_output(self.__IOREG_CHARGE_COMMAND, shell=True).decode(
            'utf-8').strip().split('=')[1].strip() == 'Yes' else False

    def __send_notification(self, title: str, current_capacity: str):
        """
        Send the notification to the Line room associated with the token using the Line Notify API.

        Args:
            title (str): The title of the message
            current_capacity (str): The current capacity of the battery
        """

        requests.post(
            self.__LINE_NOTIFY_API,
            headers={'Authorization': 'Bearer ' + self.__LINE_NOTIFY_TOKEN},
            params={'message': self.__MESSAGE_TEMPLATE.format(
                title=title,
                caution='Stop charging MacBook' if 'overcharging' in title else 'Charge MacBook',
                current_capacity=current_capacity
            ).strip()})


if __name__ == '__main__':
    pass
